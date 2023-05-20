import os
from datetime import datetime
import json

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
    f = open('card_org.json')
    # returns JSON object as 
    # a dictionary
    json_text = json.load(f)
    
    # Iterating through the json
    # list
    url_str = 'https://www.ez-nail.com/eznail_mobile_hnp/?UserLineId=U5628cbc5abb074e1eb7995aecc401c17&UserDisplayName=Jacky+Chen&SalonID=420'

    #new_data = {"uri":url_str}
    for content in json_text['footer']['contents']:
        footer_url = content['action']['uri']
        print('footer URL:%s'%footer_url)
        content['action']['uri'] = url_str
    json_data = json.dumps(json_text,indent=2)
    
    with open("output.json", "w") as file:
        file.write(json_data)


#data['footer']['contents'][0].update(new_data)
#for i in data['footer']['contents']:
#    print(i['action'])
#    i['action'].update(new_data)
#print(data['footer']['contents'])     

# Closing file
f.close()



