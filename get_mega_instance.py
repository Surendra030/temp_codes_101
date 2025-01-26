import os
import subprocess
from mega import Mega





def fetch_m():
        

    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    mega  = Mega()
    keys[0] = keys[0].replace('7@','7@')
    m = mega.login(keys[0],keys[1])
    return m

def upload_file(filename):
    m = fetch_m()
    folder_name = 'pdf_modified_videos'
    file = m.create_folder(folder_name)
    fh = file[folder_name]
    
    try:
        
        link = m.upload(filename,fh)
        if link:
            return link
        
    except Exception as e:
        print("Error : ",e)

def download_url_file(url):
    m = fetch_m()
    try:
        m.download_url(url)
        return True
    except Exception as e:
        print("Error failed to downaload :",e)

def download_file_name(file_name):
    m = fetch_m()
    try:
        link = m.export(file_name)
        if link:
            download_url_file(link)
            if os.path.exists(file_name):
                return True
        return False
 
    except Exception as e:
        print("Error failed to download file :",e)
