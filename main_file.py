from mega import Mega
import os
import json

from decrypt import decrypt_json
from upload_before_coded import upload_mkv_files
from download_video import start_downloading
from get_meta_data import meta_data_main
from hardcode_videos import hardcode_all_videos
from upload_videos import upload_hardcoded_videos_folders,deleted_all_videos
from split_video import split_video_main

# Get the password from the environment variable
key_pass = os.getenv("PASSWORD")
# Provide the correct file path (relative or absolute)
file_name = 'data_encrypted.json'


a_index = 146

# Check if the file exists before proceeding
if os.path.exists(file_name):

    data = decrypt_json(file_name, key_pass)

    folder_name_lst = []
    if len(data) > 0:
        # Select a portion of the data (e.g., element at index 145 to 146)
        main_obj = data[a_index]
        try:

            for obj in main_obj['data'][1:2]:
                start_downloading(obj)
            deleted_all_videos()
            print("All present videos deleted sucessfully...")
            
        except Exception as e:
            print(f"Error failed to download data :  {main_obj}")
        try:
            meta_data_main()
            
        except Exception as e:
            print("Error failed to get meta data : ",e)
        try:
            upload_mkv_files()
        except Exception as e:
            print("Error failed to upload video files : ",e)
        
        try:
            hardcode_all_videos()
        except Exception as e:
            print("Error failed to upload video files : ",e)
        try:
            folder_name_lst = split_video_main()
        except Exception as e:
            print("Error failed to upload video files : ",e)
                
        try:
            from upload_videos import upload_hardcoded_videos_folders
            upload_hardcoded_videos_folders(folder_name_lst)
        except Exception as e:
            print("Error failed to upload video files : ",e)
    
    
    else:
        print("No data to process in the decrypted file.")
else:
    print(f"Error: File '{file_name}' not found.")
