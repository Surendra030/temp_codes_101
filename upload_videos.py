from mega import Mega
import os
import json


keys = os.getenv("M_TOKEN")

keys = keys.split("_")
mega  = Mega()

m = mega.login(keys[0],keys[1])

def deleted_all_videos():

    keys = os.getenv("M_TOKEN")

    keys = keys.split("_")
    mega  = Mega()

    m = mega.login(keys[0],keys[1])

    all_files = m.get_files().items()
    for key,snippet in all_files:
        if snippet['t'] ==0:
            m.delete(key)
    print("All files are deleted sucessfully..")


deleted_all_videos()


def upload_hardcoded_videos_folders(folder_name_lst):
    
    for obj   in folder_name_lst:
        folder_name = obj['folder']
        file = m.create_folder(folder_name)
        f_h = file[folder_name]

        for file_name in os.listdir(folder_name):
            file_name = os.path.join(folder_name,file_name)
            m.upload(file_name,f_h)
            os.remove(file_name)

