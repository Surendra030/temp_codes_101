from mega import Mega
import os
import json
from get_mega_instance import fetch_m


def upload_hardcoded_videos_folders():
    try:
        m = fetch_m()

        print(f'{30*"*"}')
        files_lst = os.listdir()
        for index,i in enumerate(files_lst,start=1):

            print(i)
            
        print(f'{30*"*"}')


        folder_name = 'zip_files'
        file = m.create_folder(folder_name)
        for file_name in files_lst:

            if '.zip' in file_name:
                print("Zip file found ")                 
                try:
                    m.upload(file_name,file[folder_name])
                    print(f"file : {file_name} uploaded sucessfully.. ")
                    os.remove(file_name)
                except Exception as e:
                    print(f"Error uploading file '{file}': {e}")
            else: print("No zip files found.")
    except Exception as e:
        print(f"Error during upload of hardcoded video folders: {e}")

