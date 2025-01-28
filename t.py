from pydub.utils import mediainfo
from pydub import AudioSegment
from add_middle_last import add_m_l
import os
import subprocess
import json
from get_mega_instance import fetch_m

final_lst = []
fs = f"video_links_modified.json"
m = fetch_m()

all_files = m.get_files()

for key,snippet in all_files.items():
    file_name = snippet['a']['n']
    if '.mp4' in file_name:
        link = m.export(file_name)
        final_lst.append({
            'link':link,
            'file_name':file_name
        })


with open(fs,'w',encoding='utf-8')as f:
    json.dump(final_lst,f,indent=4)
m.upload(fs)