import os
from datetime import datetime

from flask import Flask, abort, request, jsonify

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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
   
    #date_par = request.ars.get('date')
    #time_par = request.args.get('time')
    name_par = request.args.get('name')
    srv_par = request.args.get('service')
    #age = int(request.args.get('age'))
    #timestr = convert_date_time(time_par)
    #text_msg ="日期:" + date_par + "\n"+ \
    #          "時間:" + time_par + "\n"+ \
    #          "姓名:" + name_par + "\n" + \
    #          "服務:" + srv_par    
    text_msg = "姓名:" + name_par + "\n" + \
               "服務:" + srv_par 
        
    try:
        line_bot_api.push_message(user_id,TextSendMessage(text=text_msg))
        return text_msg
    except LineBotApiError as e:
        print("LineBot Error:{0}".format(e.message))
    return jsonify(message=text_msg)

#@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["POST"])
def callback():

    if request.method == "GET":
        return "Welcome Linebot Salon App"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = "Happy New Year 2023,"
    get_message += event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)

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