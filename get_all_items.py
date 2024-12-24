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
    
    file_1_link = m.export('data1.json')
    
    m.download_url(file_1_link)
except Exception as e:
    print('Error failed to download file.')

with open('data.json','r',encoding='utf-8')as f:
    data1 = json.load(f)

with open('data.json1','r',encoding='utf-8')as f:
    data2 = json.load(f)


data = [{**d1, **d2} for d1 in data1 for d2 in data2]



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

# Preprocess `data` into a hash-based lookup structure
href_to_tags = {}
for main_obj in data:
    for tag_lst in main_obj:
        all_titles_obj = main_obj[tag_lst]
        for one_title_obj in all_titles_obj:
            if 'href' in one_title_obj:
                href = one_title_obj['href']
                if href not in href_to_tags:
                    href_to_tags[href] = []
                if tag_lst not in href_to_tags[href]:  # Avoid duplicates
                    href_to_tags[href].append(tag_lst)

# Use a set for `ids_data` for quick membership checks
ids_set = set(ids_data)

# Build the ids_dict
ids_dict = {}
for index, id in enumerate(ids_set):
    print(f"{index + 1}-{len(ids_set)}")
    for href, tags in href_to_tags.items():
        if id in href:  # Quick lookup using the preprocessed dictionary
            if id not in ids_dict:
                ids_dict[id] = []
            # Append unique tags
            ids_dict[id].extend(tag for tag in tags if tag not in ids_dict[id])

# Convert ids_dict to a list of dictionaries
ids_lst = [{key: value} for key, value in ids_dict.items()]

# Save the result to a JSON file
with open("ids_data.json", 'w', encoding='utf-8') as f:
    json.dump(ids_lst, f, indent=4)


m = mega.login(keys[0],keys[1])
try:
    m.upload('ids_data.json')
except Exception as e:
    print("Failed to upload file.")