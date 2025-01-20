import os
import subprocess
from mega import Mega
import re
import traceback
from get_mega_instance import fetch_m




def uplox_all_videos(file,m,f_h):
    m.upload(file,f_h)

def upload_mkv_files():

    m = fetch_m()  

    folder_name = 'temp_folder'
    file = m.create_folder(folder_name)
    f_h = file[folder_name]
    all_files = os.listdir()
    lst = []
    for file  in all_files:
        if 'hardcoded' in file or '.mp4' in file:
            lst.append(file)

    for file in lst:
        uplox_all_videos(file,m,f_h)

    print("All files are uploaded sucessfully..")
