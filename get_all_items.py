import json
from mega import Mega
import os


keys  = os.getenv("M_TOKEN")
keys= keys.split("_")

mega = Mega()
m = mega.login(keys[0],keys[1])

try:
    file_1_link = m.export('data.json')
    
    m.download_url(file_1_link)
    
   
except Exception as e:
    print('Error failed to download file.')


try:
    
    file_2_link = m.export('data1.json')
    
    m.download_url(file_2_link)
except Exception as e:
    print('Error failed to download file.')


with open('data.json','r',encoding='utf-8')as f:
    data1 = json.load(f)

with open('data1.json','r',encoding='utf-8')as f:
    data2 = json.load(f)


data = [{**d1, **d2} for d1 in data1 for d2 in data2]


with open('final_data.json','w',encoding='utf-8')as f:
    json.dump(data,f,indent=4)

all_ids = set()
for main_obj in data:
    for tag_lst in main_obj:
        all_titles_obj = main_obj[tag_lst]
        main_tag = tag_lst
        for one_title_obj in all_titles_obj:
            if 'href' in one_title_obj:
                id_part = str(one_title_obj['href']).split('.net/')[-1]
                all_ids.add(id_part)


    
ids_data = list(all_ids)

with open('ids_lst.json','w',encoding='utf-8')as f:
    json.dump(ids_data,f,indent=4)


m = mega.login(keys[0],keys[1])
try:
    m.upload('final_data.json')
    m.upload('ids_lst.json')
except Exception as e:
    print("Failed to upload file.")