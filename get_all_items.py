import json
from mega import Mega
import os
import gzip


keys  = os.getenv("M_TOKEN")
keys= keys.split("_")
keys[0] = str(keys[0]).replace('6@','7@')
mega = Mega()
m = mega.login(keys[0],keys[1])

handle = 'OdhCgTJR'

all_files1 = m.get_files()

with open("final.json",'r',encoding='utf-8')as f:
    data = json.load(f)
    



index = 1
all_files = []

for obj in data:
    for old,new in obj.items():

        for key,snippet in all_files.items():
            file_name =  snippet['a']['n']
            if snippet['p'] == handle and file_name == old:
                m.request_id(file_name,new)
                

            print(f'{index} / {len(data)}')
            index +=1



index = 1

for key,snippet in all_files1.items():
    file_name =  snippet['a']['n']
    if snippet['p'] == handle and '.mp4' in file_name:
        link = m.export(file_name)
        obj = {
            'file_name':file_name,
            'link':link
        }
        all_files.append(obj)

    print(f'{index} / {len(all_files)}')
    index +=1

try:
    with open("links_data.json",'w',encoding='utf-8')as f:
        json.dump(all_files,f,indent=4)
    if os.path.exists("links_data.json"):
        m.upload("links_data.json")
except Exception as e:
    print("Error Failed to upload.",e)
