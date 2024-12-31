import json
from mega import Mega
import os
import gzip


keys  = os.getenv("M_TOKEN")
keys= keys.split("_")
keys[0] = str(keys[0]).replace('6@','7@')
mega = Mega()
m = mega.login(keys[0],keys[1])


all_files = m.get_files()

lst = []
for key,snippet in all_files.items():
    if snippet['p'] == 'OdhCgTJR':
        file_name = snippet['a']['n']
        link = m.export(file_name)
        obj = {
            'file_name':file_name,
            'link':link
        }
        lst.append(obj)

# Step 3: Save the updated data to new.json
with open("links_data.json", 'w', encoding='utf-8') as f:
    json.dump(lst, f, indent=4)

m.upload("links_data.json")


