#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
import json
import numpy as np

#import pymongo
#from pymongo import MongoClient
#from flask_restful import Resource, Api, reqparse

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)

lineaccesstoken = '76NERDBD5qJWngbMUWEhKyCIUInU9CpCHYLoIebunqnJqk8tLuiHC0oklBHV9Qr30OoWQDdTjyVkMkvyqE7+dekajTLQSOX3NsJ/byF1EDogsOJmE+2nTYvLvpRoP9RDy/0kmVzmQ7uixgXYzXLXXgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)

####################### new ########################
@app.route('/')
def index():
    return "Hello World!"


@app.route('/callback', methods=['POST'])
def callback():
    #try:
    json_line = request.get_json(force=False,cache=False)
    #except:
    #    print('cannot get json_line')
    #    return '',200
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        #try:
        event_handle(event)
        #except:
        #    pass
    return '',200


def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
        return ''
#
    if msgType == "text":
        msg = str(event["message"]["text"])
        outmsg = textmessagehandler(msg)
        replyObj = TextSendMessage(text=outmsg)
        line_bot_api.reply_message(rtoken, replyObj)

    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''

replyDic = {}
replyDic['สวัสดี'] = 'ว่าไงจ้ะ'
replyDic['ขอโทษ'] = 'ไม่เป็นไร'

def textmessagehandler(msg):
    #msg = translatefunc(msg) #translate
    try:
        msg = replyDic[msg]
    except:
        msg = 'ไม่เข้าใจครับ'
    return msg

from googletrans import Translator
translator = Translator()

def translatefunc(msg):
    #translate from th -> en or en -> th
    lang = translator.detect(msg).lang
    if lang == 'th':
        out = translator.translate(msg,'en').text
    else:
        out = translator.translate(msg,'th').text
    return out


if __name__ == '__main__':
    app.run(debug=True)
