import os
from datetime import datetime
import json
import sys

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
if __name__ == '__main__':
    f = open('booking.json')
    # returns JSON object as 
    # a dictionary
    json_text = json.load(f)
    
    # Iterating through the json
    # list
    name_str = '小美'
    service_str = '美足'
    date_str = '2023-11-01'
    time_str = '14:00'
    #new_data = {"uri":url_str}
    for content in json_text['body']['contents']:
        if content['type'] == 'box':
            print(content['contents'][0]['text'])
            if content['contents'][0]['text'] == '姓名:':
                content['contents'][0]['text'] = content['contents'][0]['text']+name_str
            elif content['contents'][0]['text'] == '服務:':    
                content['contents'][0]['text'] = content['contents'][0]['text']+service_str 
            elif content['contents'][0]['text'] == '日期:':    
                content['contents'][0]['text'] = content['contents'][0]['text']+date_str 
            elif content['contents'][0]['text'] == '時間:':    
                content['contents'][0]['text'] = content['contents'][0]['text']+time_str 

    json_data = json.dumps(json_text,indent=2,ensure_ascii=False).encode('utf8')
    print(json_data.decode())

    with open('output.json', 'w', encoding='utf8') as json_file:
        json.dump(json_text,json_file,ensure_ascii=False)
      

    # Closing file
    f.close()



