import json
from mega import Mega
import os
import gzip


keys  = os.getenv("M_TOKEN")
keys= keys.split("_")
keys[0] = str(keys[0]).replace('6@','7@')
mega = Mega()
m = mega.login(keys[0],keys[1])

try:
    
    m.download_url('https://mega.nz/file/1lRBSQIZ#CA2551RiAPjagk_P7UKRfinyc_FLQzP_EFM_fEkUdhM')
    
   
except Exception as e:
    print('Error failed to download file.')


try:
    
    
    m.download_url('https://mega.nz/file/t1JgzIrD#TruZDnPBu94QLU0PWuIYyBLa1kFLM0DPYreVzwdF04Q')
except Exception as e:
    print('Error failed to download file.')


print(os.listdir())
with open('data.json','r',encoding='utf-8')as f:
    data1 = json.load(f)

with open('data1.json','r',encoding='utf-8')as f:
    data2 = json.load(f)



data = [{**d1, **d2} for d1 in data1 for d2 in data2]


# Save and compress the JSON file
compressed_file = 'final_data_json.gz'

with gzip.open(compressed_file, 'wb') as f:
    json_str = json.dumps(data, indent=4)  # Convert the JSON data to a string
    f.write(json_str.encode('utf-8'))  # Compress and save the JSON string as binary

print(f"Compressed JSON file saved as: {compressed_file}")

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

keys[0] = str(keys[0]).replace('6@','7@')

m = mega.login(keys[0],keys[1])
try:
    if os.path.exists(compressed_file):
        print("filesize : ",os.path.getsize(compressed_file))
        m.upload(compressed_file)
except Exception as e:
    print("Failed to upload file.")

try:
    
    m.upload('ids_lst.json')
except Exception as e:
    print("Failed to upload id-file.")