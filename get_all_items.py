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

        for key,snippet in all_files1.items():
            file_name =  snippet['a']['n']
            if snippet['p'] == handle and file_name == old:
                m.rename(file_name,new)
                

            print(f'{index} / {len(data)}')
            index +=1


