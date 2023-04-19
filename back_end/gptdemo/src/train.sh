# v100-16g x 4, fp16-O1, 2.0h
# 2080ti-11g x 4, fp16-O1, 2.5h
../../environment/demo/bin/python -m torch.distributed.launch \
--nproc_per_node 4 --master_port 56789 train.py \
--pretrained \
--model_checkpoint ../pretrain_models/CDial-GPT_LCCC-large \
--data_path ../data-douban/douban_train_valid.json \
--dataset_cache dataset_cache/douban \
--n_epochs 10 \
--train_batch_size 8 \
--valid_batch_size 8 \
--scheduler linear_warmup \
--lr 5e-5 \
--warmup_steps 10000 \
--valid_steps 5000 \
--gradient_accumulation_steps 64 \
--max_norm 1.0 \
--fp16 O1


# v100-16g x 2, fp16-O1, 时间未知
../../environment/demo/bin/python -m torch.distributed.launch \
--nproc_per_node 2 --master_port 56789 train.py \
--pretrained \
--model_checkpoint ../pretrain_models/CDial-GPT_LCCC-large \
--data_path ../data-douban/douban_train_valid.json \
--dataset_cache dataset_cache/douban \
--n_epochs 10 \
--train_batch_size 8 \
--valid_batch_size 8 \
--scheduler linear_warmup \
--lr 5e-5 \
--warmup_steps 10000 \
--valid_steps 5000 \
--gradient_accumulation_steps 128 \
--max_norm 1.0 \
--fp16 O1


# v100-16g x 1, fp16-O1, 时间未知
../../environment/demo/bin/python train.py \
--pretrained \
--model_checkpoint ../pretrain_models/CDial-GPT_LCCC-large \
--data_path ../data-douban/douban_train_valid.json \
--dataset_cache dataset_cache/douban \
--n_epochs 10 \
--train_batch_size 8 \
--valid_batch_size 8 \
--scheduler linear_warmup \
--lr 5e-5 \
--warmup_steps 10000 \
--valid_steps 5000 \
--gradient_accumulation_steps 256 \
--max_norm 1.0 \
--fp16 O1
