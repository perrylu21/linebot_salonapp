import os
from datetime import datetime

from flask import Flask, abort, request, jsonify

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
user_id = U993e4bed50c6b80ac697b078fda84a01

@app.route("/",methods=["GET"])
def get_params():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    text_msg ="My name is " + name + " and I am " + str(age) + " years old" 
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
    get_message = "Happy 2023,"
    get_message += event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
