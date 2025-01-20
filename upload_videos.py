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
        for file in files_lst:

            if '.zip' in file:
                                    
                try:
                    m.upload(file,file[folder_name])

                    os.remove(file)
                    print(f"file : {file} uploaded sucessfully.. ")
                except Exception as e:
                    print(f"Error uploading/removing file '{file}': {e}")
 
    except Exception as e:
        print(f"Error during upload of hardcoded video folders: {e}")

