import os
import logging
import random
from itertools import chain
from argparse import ArgumentParser
from pprint import pformat
import time
import torch
import torch.nn.functional as F
import math
from .src.transformers import OpenAIGPTLMHeadModel, GPT2LMHeadModel, BertTokenizer
from .src.singleton_model import singleton


@singleton
class MODEL_REPLY_GPT():
    
    def __init__(self):
        self.SPECIAL_TOKENS = ["[CLS]", "[SEP]", "[PAD]", "[speaker1]", "[speaker2]"]
        args = self.get_args()
        self.args=args
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__file__)
        self.logger.info(pformat(args))
        random.seed(args.seed)
        torch.random.manual_seed(args.seed)

        self.logger.info("Get pretrained model and tokenizer")
        tokenizer_class = BertTokenizer
        model_class = OpenAIGPTLMHeadModel if not args.gpt2 else GPT2LMHeadModel
        never_split = ["[neutral]", "[happiness]", "[sadness]", "[anger]", "[disgust]"]
        self.tokenizer = tokenizer_class.from_pretrained(args.model_checkpoint, do_lower_case=True, never_split=never_split)
        self.tokenizer.additional_special_tokens = never_split
        self.model = model_class.from_pretrained(args.model_checkpoint)
        self.model.to(args.device)
        self.model.eval()

        self.emotion_map = {"n": 13081, "h": 13082, "s": 13083, "a": 13084, "d": 13085}
        self.emotion_map_ = {13081: "[neutral]", 13082: "[happiness]", 13083: "[sadness]", 13084: "[anger]", 13085: "[disgust]"}
        
        self.emotion = 13081

        self.bad_word_ch=['傻逼', '你妹', '卧槽', '讨厌你', '你大爷', '滚粗', '哈哈','草泥马','婊子','滚']
        self.bad_word=[]
        for line in self.bad_word_ch:
            temp=self.tokenizer.tokenize(line)
            self.bad_word.append(self.tokenizer.convert_tokens_to_ids(temp))
    def get_args(self):
        parser = ArgumentParser()
        parser.add_argument('--gpt2', action='store_true', help="use gpt2")
        parser.add_argument("--model_checkpoint", type=str, default="./gpt_reply_model/checkpoints/runs/Mar20_14-13-06_gpu20", help="Path, url or short name of the model")
        parser.add_argument("--max_history", type=int, default=4, help="Number of previous utterances to keep in history")
        parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu",
                            help="Device (cuda or cpu)")

        parser.add_argument("--no_sample", action='store_true', help="Set to use greedy decoding instead of sampling")
        parser.add_argument("--max_length", type=int, default=30, help="Maximum length of the output utterances")
        parser.add_argument("--min_length", type=int, default=1, help="Minimum length of the output utterances")
        parser.add_argument("--seed", type=int, default=42, help="Seed")
        parser.add_argument("--temperature", type=int, default=0.7, help="Sampling softmax temperature")
        parser.add_argument("--top_k", type=int, default=0, help="Filter top-k tokens before sampling (<=0: no filtering)")
        parser.add_argument("--top_p", type=float, default=0.9,
                            help="Nucleus filtering (top-p) before sampling (<=0.0: no filtering)")
        args = parser.parse_args(args=[])
        return args
    def tokenize(self,obj):
        if isinstance(obj, str):
            return self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(obj))
        if isinstance(obj, dict):
            return dict((n, tokenize(o)) for n, o in obj.items())
        return list(tokenize(o) for o in obj)


    def top_filtering(self,logits, top_k=0, top_p=0.0, threshold=-float('Inf'), filter_value=-float('Inf')):
        
        assert logits.dim() == 1  # Only work for batch size 1 for now - could update but it would obfuscate a bit the code
        top_k = min(top_k, logits.size(-1))
        if top_k > 0:
            # Remove all tokens with a probability less than the last token in the top-k tokens
            indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
            logits[indices_to_remove] = filter_value

        if top_p > 0.0:
            # Compute cumulative probabilities of sorted tokens
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probabilities = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

            # Remove tokens with cumulative probability above the threshold
            sorted_indices_to_remove = cumulative_probabilities > top_p
            # Shift the indices to the right to keep also the first token above the threshold
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            # Back to unsorted indices and set them to -infinity
            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            logits[indices_to_remove] = filter_value

        indices_to_remove = logits < threshold
        logits[indices_to_remove] = filter_value

        return logits



    def build_input_from_segments(self,history, reply, tokenizer, with_eos=True):
        """ Build a sequence of input from 3 segments: persona, history and last reply """
        bos, eos, pad, speaker1, speaker2 = tokenizer.convert_tokens_to_ids(self.SPECIAL_TOKENS)
        sequence = [[bos]] + history + [reply + ([eos] if with_eos else [])]
        sequence = [sequence[0]] + [[speaker2 if i % 2 else speaker1] + s for i, s in enumerate(sequence[1:])]
        print(sequence)
        instance = {}
        instance["input_ids"] = list(chain(*sequence))
        instance["token_type_ids"] = [bos] + [speaker2 if i % 2 else speaker1 for i, s in enumerate(sequence[1:])
                                            for _ in s]
        return instance, sequence


    def sample_sequence(self,history, tokenizer, model, args, current_output=None):
        special_tokens_ids = tokenizer.convert_tokens_to_ids(self.SPECIAL_TOKENS)
        if current_output is None:
            current_output = []
        args=self.args
        for i in range(args.max_length):
            instance, sequence = self.build_input_from_segments(history, current_output, tokenizer, with_eos=False)
            input_ids = torch.tensor(instance["input_ids"], dtype=torch.long, device=args.device).unsqueeze(0)
            token_type_ids = torch.tensor(instance["token_type_ids"], dtype=torch.long, device=args.device).unsqueeze(0)

            logits, *_ = model(input_ids, token_type_ids=token_type_ids)
            logits = logits[0, -1, :] / args.temperature
            logits = self.top_filtering(logits, top_k=args.top_k, top_p=args.top_p)
            probs = F.softmax(logits, dim=-1)

            prev = torch.topk(probs, 1)[1] if args.no_sample else torch.multinomial(probs, 1)
            if i < args.min_length and prev.item() in special_tokens_ids:
                while prev.item() in special_tokens_ids:
                    prev = torch.multinomial(probs, num_samples=1)

            if prev.item() in special_tokens_ids:
                break
            current_output.append(prev.item())

        return current_output


    def beam_search_squenece_2(self,history, tokenizer, model, args, beam=2, current_output=None):
        special_tokens_ids = tokenizer.convert_tokens_to_ids(self.SPECIAL_TOKENS)
        if current_output is None:
            beam_output, beam_prob = [], []
            ans_output, ans_prob = [], []
            probs, prev = self.get_word(history, [], tokenizer, model, args)
            for i in range(beam):
                if prev[i] not in special_tokens_ids and probs[prev[i].item()].item()>1e-9:
                    beam_output.append([prev[i].item()])
                    beam_prob.append(probs[prev[i].item()].item())
        else:
            beam_output, beam_prob = [current_output], [1]
            ans_output, ans_prob = [], []
            #生成第一步
        for step in range(args.max_length):#开始搜索，深度为max_leangth
            next_beam_output, next_beam_prob = [], []
            for current_output, current_prob in zip(beam_output, beam_prob):
                probs, prev = self.get_word(history, current_output, tokenizer, model, args)
                for word in prev:
                    word = word.item()
                    if word in special_tokens_ids and step > args.min_length: #可以终止
                        if current_prob * (probs[word].item()) > 1e-9:#终止令牌是否恰当
                            ans_output.append(current_output)
                            ans_prob.append(current_prob)
                    elif word in special_tokens_ids: #不能终止
                        continue
                    else:
                        if not self.is_sensitive(tokenizer.decode(current_output + [word], skip_special_tokens=True)):
                            if current_prob * (probs[word].item())>1e-9:
                                next_beam_output.append(current_output + [word])
                                next_beam_prob.append(current_prob * (probs[word].item())) #下一回搜索
            if len(next_beam_prob) == 0:
                break  # 没东西生成了滚蛋吧
            seq_k = torch.topk(torch.Tensor(next_beam_prob), beam)[1] if len(next_beam_output) > beam else torch.Tensor(
                range(len(next_beam_output)))  # 拿出前beamgay率，只搜索前Beam个
            beam_output, beam_prob = [], []
            for i in seq_k:
                beam_output.append(next_beam_output[int(i.item())])
                beam_prob.append(next_beam_prob[int(i.item())])
        ans_output, ans_prob = ans_output + beam_output, ans_prob + beam_prob
        print(len(ans_output))
        ans_prob = [math.log(ans_prob[i])/len(ans_output) for i in range(len(ans_prob))]#保证不会过短
        return ans_output[torch.multinomial(F.softmax(torch.tensor(ans_prob).reshape(1, -1),dim=1), 1).item()]


    def get_word(self,history, current_output, tokenizer, model, args, top_k=2):
        instance, sequence = self.build_input_from_segments(history, current_output, tokenizer, with_eos=False)
        input_ids = torch.tensor(instance["input_ids"], dtype=torch.long, device=args.device).unsqueeze(0)
        token_type_ids = torch.tensor(instance["token_type_ids"], dtype=torch.long, device=args.device).unsqueeze(0)
        logits, *_ = model(input_ids, token_type_ids=token_type_ids)
        logits = logits[0, -1, :] / args.temperature  # 取最后一个时间段新产生的令牌？
        logits = self.top_filtering(logits, top_k=top_k, top_p=args.top_p)
        probs = F.softmax(logits, dim=-1)
        prev = torch.topk(probs, top_k, sorted=True)[1]  # 降序排序,要索引
        return probs, prev


    def is_sensitive(self,seq):
        seq = ''.join(seq.split(' '))
        for word in self.bad_word_ch:
            if word in seq:
                print(seq)
                return True
        return False

    def get_history(self,userid):
        history = [[self.emotion]]
        userid=str(userid)
        massage_path=os.path.join('../video_data_from_frontend',userid,'massage.log')
        with open(massage_path,'r') as f:
            for line in f:
                line=line.strip()
                history.append(self.tokenize(line))
                history = history[0:1] + history[1:][-(2 * self.args.max_history + 1):]
                print(self.emotion_map_[history[0][0]], history[1:])
        return history

    def reply_generate(self,userid,emotion):
        self.emotion=self.emotion_map[emotion]
        history=self.get_history(userid)
        old_time=time.time()
        with torch.no_grad():
            if self.emotion_map_[self.emotion][1] in ['n','h','s']:
                out_ids = self.sample_sequence(history, self.tokenizer, self.model, self.args)
            else:
                out_ids = self.beam_search_squenece_2(history, self.tokenizer, self.model, self.args)
            # out_ids = self.beam_search_squenece_2(history, self.tokenizer, self.model, self.args)
            # out_ids = self.sample_sequence(history, self.tokenizer, self.model, self.args)
            history.append(out_ids)
        cost_time=time.time()-old_time
        out_text = self.tokenizer.decode(out_ids, skip_special_tokens=True)
        out_text=out_text.replace(" ", "")
        massage_path=os.path.join('../video_data_from_frontend',userid,'massage.log')
        with open(massage_path,'a') as f:
            f.write(out_text+'\n')
        return out_text,cost_time
    
model_reply_gpt=MODEL_REPLY_GPT()
    


