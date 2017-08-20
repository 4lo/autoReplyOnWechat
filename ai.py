#coding=utf8
import re
import time
import requests

import itchat
from itchat.content import *

@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING, RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    if msg['Type'] == 'Text':
        reply_content = msg['Text']
    elif msg['Type'] == 'Picture':
        reply_content = r"图片: " + msg['FileName']
    elif msg['Type'] == 'Card':
        reply_content = r" " + msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,
                                                                                                                    2,
                                                                                                                    3)
        if location is None:
            reply_content = r"位置: 纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            reply_content = r"位置: " + location
    elif msg['Type'] == 'Note':
        reply_content = r"通知"
    elif msg['Type'] == 'Sharing':
        reply_content = r"分享"
    elif msg['Type'] == 'Recording':
        reply_content = r"语音"
    elif msg['Type'] == 'Attachment':
        reply_content = r"文件: " + msg['FileName']
    elif msg['Type'] == 'Video':
        reply_content = r"视频: " + msg['FileName']
    else:
        reply_content = r"消息"

    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '8edce3ce905a4c1dbb965e6b35c3834d',  # 如果这个Tuling Key不能用，那就换一个
        'info': r'【%s】'% reply_content,  # 这是我们发出去的消息
        'userid': 'wechat-robot',  # 这里你想改什么都可以
    }
    # 我们通过如下命令发送一个post请求
    r = requests.post(apiUrl, data=data).json()

    itchat.send(r"%s" % r['text'],
                toUserName=msg['FromUserName'])

itchat.auto_login(enableCmdQR=True)
itchat.run()
