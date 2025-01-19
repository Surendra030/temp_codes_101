import os
import subprocess
from mega import Mega
import re
import traceback





def uplox_all_videos(file,m):


    m.upload(file)

def upload_mkv_files():
    keys = os.getenv("M_TOKEN")

    keys = keys.split("_")
    mega  = Mega()
    keys[0] = keys[0].replace('6@','8@')
    m = mega.login(keys[0],keys[1])     

    all_files = os.listdir()
    lst = []
    for file  in all_files:
        if '.mkv' in file or '.mp4' in file:
            lst.append(file)

    for file in lst:
        uplox_all_videos(file,m)

    print("All files are uploaded sucessfully..")
