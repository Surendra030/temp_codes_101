from final import main_fun
from mega import Mega
import os
import json
from decrypt import decrypt_json

key_pass = os.getenv("PASSWORD")

file_name = 'data_encrypted.json'
data = decrypt_json(file_name,key_pass)

if len(data)>0:
        
    obj = data[145:146]


    main_fun(obj[0])