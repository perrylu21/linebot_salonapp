import os
from datetime import datetime
import requests
from flask import Flask, abort, request, jsonify
import json
# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
import csv
import configparser
import numpy as np

app = Flask(__name__)

#line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
#handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
#user_id = "U993e4bed50c6b80ac697b078fda84a01"
#config = configparser.ConfigParser()
#config.read('config.ini')

#line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
#handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
#user_id = config.get('line-bot', 'user_id')

# @app.route("/",methods=["GET"])
# def get_params():
#     print('get_params...')
#     name_par = request.args.get('name')
#     srv_par = request.args.get('service')
#     startdt_par = request.args.get('start')
#     enddt_par = request.args.get('end')    
#     memo_par = request.args.get('memo')
#     lineid_par = request.args.get('lineid')
#     salon_id_par = request.args.get('salonId') #WebHook default params
#     print('salonID:%s'%salon_id_par)
 
#     text_msg = "姓名:" + name_par + "\n" + \
#                "服務:" + srv_par + "\n" + \
#                "開始:" + startdt_par + "\n" + \
#                "結束:" + enddt_par + "\n" + \
#                "備註:" + memo_par + "\n"        
#     print(text_msg) 
    
#     #load booking json template and update booking info
#     f = open('booking.json')
#     # returns JSON object as a dictionary
#     json_text = json.load(f)
#     for content in json_text['body']['contents']:
#         if content['type'] == 'box':
#             print(content['contents'][0]['text'])
#             if content['contents'][0]['text'] == '姓名:':
#                 content['contents'][0]['text'] = content['contents'][0]['text']+name_par
#             elif content['contents'][0]['text'] == '服務:':    
#                 content['contents'][0]['text'] = content['contents'][0]['text']+srv_par 
#             elif content['contents'][0]['text'] == '開始:':    
#                 content['contents'][0]['text'] = content['contents'][0]['text']+startdt_par 
#             elif content['contents'][0]['text'] == '結束:':    
#                 content['contents'][0]['text'] = content['contents'][0]['text']+enddt_par 
#             elif content['contents'][0]['text'] == '備註:':    
#                 content['contents'][0]['text'] = content['contents'][0]['text']+memo_par 

#     #json_data = json.dumps(json_text,indent=2)    
#     json_data = json.dumps(json_text,indent=2,ensure_ascii=False).encode('utf8')
#     print(json_data.decode())
#     f.close()
#     with open('booking_new.json', 'w', encoding='utf8') as json_file:
#         json.dump(json_text,json_file,ensure_ascii=False)
    
#     #execute push message   
#     #token, secret = get_salon_info(salon_id_par)
#     #print('\nToken: %s'%token)
#     #line_bot_api = LineBotApi(token)
#     try:
#         #line_bot_api.push_message(lineid_par,TextSendMessage(text=text_msg))
#         FlexMessage = json.load(open('booking_new.json','r',encoding='utf-8'))
#         line_bot_api.push_message(lineid_par,FlexSendMessage('booking',FlexMessage)) 

#         return text_msg
#     except LineBotApiError as e:
#         print("LineBot Error:{0}".format(e.message))
#     return jsonify(message=text_msg)

@app.route("/", methods=["GET", "POST"])
#@app.route("/", methods=["POST"])
def callback():
    salon_id = request.args.get('salonId') #WebHook default params
    print('salonID:%s'%salon_id)
    token, secret = get_salon_info(salon_id)
    print('\nToken: %s,Secret: %s'%(token,secret))
    line_bot_api = LineBotApi(token)
    handler = WebhookHandler(secret)    
    ##write salon_id in webHook to init file 
    #config['line-bot']['salon_id'] = salon_id
    #with open('config.ini', 'w') as configfile:
    #    config.write(configfile)
        
    if request.method == "GET":
        print('Get Request...')
        name_par = request.args.get('name')
        srv_par = request.args.get('service')
        startdt_par = request.args.get('start')
        enddt_par = request.args.get('end')    
        memo_par = request.args.get('memo')
        lineid_par = request.args.get('lineid')
 
        text_msg = "姓名:" + name_par + "\n" + \
                   "服務:" + srv_par + "\n" + \
                   "開始:" + startdt_par + "\n" + \
                   "結束:" + enddt_par + "\n" + \
                   "備註:" + memo_par + "\n"        
        print(text_msg) 
    
        #load booking json template and update booking info
        f = open('booking.json')
        # returns JSON object as a dictionary
        json_text = json.load(f)
        for content in json_text['body']['contents']:
            if content['type'] == 'box':
                print(content['contents'][0]['text'])
                if content['contents'][0]['text'] == '姓名:':
                    content['contents'][0]['text'] = content['contents'][0]['text']+name_par
                elif content['contents'][0]['text'] == '服務:':    
                    content['contents'][0]['text'] = content['contents'][0]['text']+srv_par 
                elif content['contents'][0]['text'] == '開始:':    
                    content['contents'][0]['text'] = content['contents'][0]['text']+startdt_par 
                elif content['contents'][0]['text'] == '結束:':    
                    content['contents'][0]['text'] = content['contents'][0]['text']+enddt_par 
                elif content['contents'][0]['text'] == '備註:':    
                    content['contents'][0]['text'] = content['contents'][0]['text']+memo_par 
        #create booking Flex Message 
        json_data = json.dumps(json_text,indent=2,ensure_ascii=False).encode('utf8')
        print(json_data.decode())
        f.close()
        with open('booking_new.json', 'w', encoding='utf8') as json_file:
            json.dump(json_text,json_file,ensure_ascii=False)
    
        #execute push message   

        try:
            #line_bot_api.push_message(lineid_par,TextSendMessage(text=text_msg))
            print('lineid_par:%s'%lineid_par)
            FlexMessage = json.load(open('booking_new.json','r',encoding='utf-8'))
            line_bot_api.push_message(lineid_par,FlexSendMessage('booking',FlexMessage)) 

            return text_msg
        except LineBotApiError as e:
            print("LineBot Error:{0}".format(e.message))
        return jsonify(message=text_msg)        
    if request.method == "POST":
        print('Post Request...')
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        json_data = json.loads(body)
        try:
            handler.handle(body, signature)
            print('json_data:\n')
            print(json_data)
            title_message = "Thanks for using iSalonbot, "
            message_text = json_data['events'][0]['message']['text'] 
            print('message text:%s'%message_text)
            if message_text == '線上預約':
                message_type = json_data['events'][0]['message']['type'] 
                reply_token = json_data['events'][0]['replyToken']
                user_id = json_data['events'][0]['source']['userId']

                user_profile = line_bot_api.get_profile(user_id)
                print('Profile:')
                print(user_profile)

                #salon_id = config.get('line-bot', 'salon_id')
                #"https://www.ez-nail.com/eznail_mobile_hnp/?UserLineId=U5628cbc5abb074e1eb7995aecc401c17&UserDisplayName=Jacky+Chen&SalonID=420"
                url_string = 'https://www.ez-nail.com/eznail_mobile_hnp/'+'?UserLineId='+user_profile.user_id+'&'\
                        + 'SalonID=' + salon_id
                print(url_string)
                UpdateFlexMessageURL('card_org.json', 'card_new.json', url_string)
                            
                #display flex message menu with linebot
                FlexMessage = json.load(open('card_new.json','r',encoding='utf-8'))
                line_bot_api.reply_message(reply_token, FlexSendMessage('profile',FlexMessage))
                #pass user id to iSalon web app
                user_data = {'UserLineId':user_profile.user_id,'SalonID':salon_id}

                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                #response = requests.post('https://www.ez-nail.com/eznail_mobile_hnp/',
                #    data=json.dumps(user_data),headers=headers)
                response = requests.get('https://www.ez-nail.com/eznail_mobile_hnp/',
                    params=user_data,headers=headers)
            
                print('response_status:%d'%response.status_code)
                #print(response.url)
                #print(response.text)     
            else:
                print('Unsuppoted message text.')    
       
      
        except InvalidSignatureError:
            print('Invalid Signature Error')
            abort(400)

        return "OK"


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     get_message = "Thanks for using iSalonbot, "
#     get_message += event.message.text
#     message_type = event.message.type
#     reply_token = event.reply_token    
#     user_id = event.source.user_id 
#     try:
#         user_profile = line_bot_api.get_profile(user_id)
#         print('Profile:')
#         print(user_profile)
#         #User Display name may contain white space, need to trim space
#         #user_display_str = user_profile.display_name 
#         #user_display_str = user_display_str.replace(" ","")
#         #print(user_display_str)
#         salon_id = config.get('line-bot', 'salon_id')
#         #"https://www.ez-nail.com/eznail_mobile_hnp/?UserLineId=U5628cbc5abb074e1eb7995aecc401c17&UserDisplayName=Jacky+Chen&SalonID=420"
#         url_string = 'https://www.ez-nail.com/eznail_mobile_hnp/'+'?UserLineId='+user_profile.user_id+'&'\
#                     + 'SalonID=' + salon_id
#         print(url_string)
#         UpdateFlexMessageURL('card_org.json', 'card_new.json', url_string)
                        
#         #display flex message menu with linebot
#         FlexMessage = json.load(open('card_new.json','r',encoding='utf-8'))
#         line_bot_api.reply_message(reply_token, FlexSendMessage('profile',FlexMessage))
#         #pass user id to iSalon web app
#         user_data = {'UserLineId':user_profile.user_id,'SalonID':salon_id}

#         headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#         #response = requests.post('https://www.ez-nail.com/eznail_mobile_hnp/',
#         #    data=json.dumps(user_data),headers=headers)
#         response = requests.get('https://www.ez-nail.com/eznail_mobile_hnp/',
#             params=user_data,headers=headers)
        
#         print(response.status_code)
#         print(user_data)
#         print(response.url)
#         #print(response.text)
        
#     except:
#         print('Fail to reply message.')

    
def UpdateFlexMessageURL(JsonInFile, JsonOutFile, url_str):
    f = open(JsonInFile)
    # returns JSON object as 
    # a dictionary
    json_text = json.load(f)
    
    # Iterating through the json
    # list

    for content in json_text['footer']['contents']:
        footer_url = content['action']['uri']
        print('footer URL:%s'%footer_url)
        content['action']['uri'] = url_str
    json_data = json.dumps(json_text,indent=2)
    
    with open(JsonOutFile, "w") as file:
        file.write(json_data)    
    f.close()    
    
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

def get_salon_info(salon_id_str):
    channel_token_str = 'none'
    channel_secret_str = 'none'
    with open('salon_config.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['salonid'] == salon_id_str:
                #print(row['salonid'], row['channel_access_token'],row['channel_access_secret'],row['salon_name'])
                return row['channel_access_token'],row['channel_access_secret']
        return channel_token_str, channel_secret_str   
       
if __name__ == "__main__":
    app.run()    