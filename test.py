from mega import Mega
from get_mega_instance import fetch_m
import json
m = fetch_m()

all_files = m.get_files().items()

links_lst = []

for key,snippet in all_files:
    
    file_name= snippet['a']['n']
    if '.pdf' in file_name:
        try:
            
            link = m.export(file_name)
        except Exception as e:
            print("Error failed :",e)
            
        obj = {
            'file_name':file_name,
            'link':link
        }
        links_lst.append(obj)

t = "pdf_links_data.json"
with open(t,'w',encoding='utf-8')as f:
    json.dump(links_lst,f,indent=4)

m.upload(t)