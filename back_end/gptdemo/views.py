import os
import json
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .model_reply import model_reply_gpt
# Create your views here.
def write(str):
    with open('out.txt','a') as f:
        f.write(str)
        f.write('\n')
@csrf_exempt
def reply_look(request):
    userID=str(request.META.get('HTTP_USERID'))
    response={}
    response['result']='reply_look ok'
    response['msg'] = 'success'
    response['error_num'] = 0
    return JsonResponse(response)

@csrf_exempt
def reply_generate(request):
    userID=str(request.META.get('HTTP_USERID'))
    body=json.loads(request.body)
    emotion=body['emotion']
    print(emotion)
    reply,cost_time=model_reply_gpt.reply_generate(userID,emotion)
    print('输出为：'+str(reply))
    data={}
    data['reply']=reply
    data['text']='userID:'+userID
    response={}
    response['data']=data
    response['msg'] = 'success'
    response['reply_model_cost_time'] = cost_time
    response['error_num'] = 0
    return JsonResponse(response)


@csrf_exempt
def send_text_and_reply_generate(request):
    userID=str(request.META.get('HTTP_USERID'))
    body=json.loads(request.body)
    text=body['massage']
    emotion=body['emotion']
    print(text)
    print(emotion)
    massage_path=os.path.join('../video_data_from_frontend',userID)
    if not os.path.exists(massage_path):
        os.mkdir(massage_path)
    with open(os.path.join(massage_path,'massage.log'),'a+') as f:
        f.write(text+'\n')
    reply,cost_time=model_reply_gpt.reply_generate(userID,emotion)
    
    data={}
    data['reply']=reply
    data['text']='userID:'+userID
    response={}
    response['data']=data
    response['msg'] = 'success'
    response['reply_model_cost_time'] = cost_time
    response['error_num'] = 0
    print(response)
    return JsonResponse(response)


