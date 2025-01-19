import os
import subprocess
from mega import Mega
import re
import traceback
from get_mega_instance import fetch_m




def uplox_all_videos(file,m):
    m.upload(file)

def upload_mkv_files():
    m = fetch_m()    

    all_files = os.listdir()
    lst = []
    for file  in all_files:
        if '.mkv' in file or '.mp4' in file:
            lst.append(file)

    for file in lst:
        uplox_all_videos(file,m)

    print("All files are uploaded sucessfully..")
