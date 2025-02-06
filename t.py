from pydub.utils import mediainfo
from pydub import AudioSegment
from add_middle_last import add_m_l
import os
import subprocess
import json
from get_mega_instance import fetch_m


m = fetch_m()

all_files = m.get_files().items()

lst = []
try:
        
    for key,snippet in all_files:
        
        fle_name=snippet['a']['n']
        if '.pdf' in fle_name:
            try:
                
                fobj = m.find(fle_name)
                link = m.export(fobj)
                obj ={
                "file_name":fle_name,
                "link":link
            }
                lst.append(obj)
            except Exception as e:
                print("error : ",e)


finally:
    
    with open("temp.json",'w')as f:
        json.dump(lst,f,indent=4)
    ms = fetch_m()
    ms.upload("temp.json")