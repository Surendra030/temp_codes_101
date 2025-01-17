from final import main_fun
from mega import Mega
import os
import json
keys = os.getenv('M_TOKEN')
keys = keys.split("_")

mega = Mega()
m = mega.login(keys[0],keys[1])
file_name = 'data_file.json'
try:
    link = m.export(file_name)
    if link:
        m.download_url(link)
except Exception as e:
    print("Error failed to downlaod file : ",e)

with open(file_name,'r',encoding='utf')as f:
    data = json.load(f)

obj = data[145:146]


main_fun(obj)