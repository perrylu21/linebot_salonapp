import os
from datetime import datetime
import requests
from flask import Flask, abort, request, jsonify
import json
# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import configparser

app = Flask(__name__)

#line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
#handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
#user_id = "U993e4bed50c6b80ac697b078fda84a01"
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
user_id = config.get('line-bot', 'user_id')

@app.route("/",methods=["GET"])
def get_params():
    print('get_params...')
    date_par = request.args.get('date')
    time_par = request.args.get('time')
    name_par = request.args.get('name')
    srv_par = request.args.get('service')
    #age = int(request.args.get('age'))
    #timestr = convert_date_time(time_par)
    #text_msg ="日期:" + date_par + "\n"+ \
    #          "時間:" + time_par + "\n"+ \
    #          "姓名:" + name_par + "\n" + \
    #          "服務:" + srv_par    
    text_msg = "姓名:" + name_par + "\n" + \
               "服務:" + srv_par + "\n" + \
               "日期:" + date_par + "\n" + \
               "時間:" + time_par + "\n"    
        
    try:
        line_bot_api.push_message(user_id,TextSendMessage(text=text_msg))
        #line_bot_api.reply_message()
        return text_msg
    except LineBotApiError as e:
        print("LineBot Error:{0}".format(e.message))
    return jsonify(message=text_msg)

@app.route("/", methods=["GET", "POST"])
#@app.route("/", methods=["POST"])
def callback():

    if request.method == "GET":
        return "Welcome to Linebot iSalon App"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print('Invalid Signature Error')
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = "Thanks for using iSalonbot, "
    get_message += event.message.text
    message_type = event.message.type
    reply_token = event.reply_token    
    user_id = event.source.user_id 
    #try:
    user_profile = line_bot_api.get_profile(user_id)
    print(user_profile)
    #display flex message menu with linebot
    FlexMessage = json.load(open('card.json','r',encoding='utf-8'))
    line_bot_api.reply_message(reply_token, FlexSendMessage('profile',FlexMessage))
    #pass user id to iSalon web app
    #params = {'UserDisplayName': user_profile.displayName, 'UserLineId':user_profile.userId, }
    params = {'UserLineId':user_profile.user_id,'UserDisplayName': user_profile.display_name}
    response = requests.post('https://www.ez-nail.com/eznail_mobile_hnp/',
        data=params)
    print(response.status_code)
    print(response.url)
    #print(response.text)
        
    #except:
    #    print('Fail to reply message.')
    # Send To Line
    #reply_msg = TextSendMessage(text=f"{get_message}")
    #line_bot_api.reply_message(event.reply_token, reply_msg)
    
    
def convert_date_time(timestr):
    #ex
    #2023-01-03-14-25-00 => 2023/01/03 14:25:00
    slist = list(timestr)
    for i,c in enumerate(slist):
        if i == 4 or i == 7:
            slist[i] = '/'
        elif i == 10:
            slist[i] = ' '
        elif i == 13 or i == 16:
            slist[i] = ':'
    s = ''.join(slist)    
    print(s)