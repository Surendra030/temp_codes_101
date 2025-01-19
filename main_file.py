from mega import Mega
import os
import json

from decrypt import decrypt_json
from upload_before_coded import upload_mkv_files
from download_video import start_downloading
from get_meta_data import meta_data_main
from hardcode_videos import hardcode_all_videos
from upload_videos import upload_hardcoded_videos_folders, deleted_all_videos
from split_video import split_video_main

# Get the password from the environment variable
key_pass = os.getenv("PASSWORD", "noText!")
print(f"Using decryption key: {key_pass}")

# Provide the correct file path (relative or absolute)
file_name = 'data_encrypted.json'
print(f"Checking if the file '{file_name}' exists...")

a_index = 146

# Check if the file exists before proceeding
if os.path.exists(file_name):
    print(f"File '{file_name}' found. Starting decryption process...")
    data = decrypt_json(file_name, key_pass)

    folder_name_lst = []
    if len(data) > 0:
        print(f"Decrypted data successfully. Processing data at index {a_index}...")
        main_obj = data[a_index]
        try:
            print("Deleting all present videos...")
            deleted_all_videos()
            print("All present videos deleted successfully.")
        except Exception as e:
            print(f"Error while deleting videos: {e}")
        for obj in main_obj['data'][1:]:
            try:  
                try:
                    print("Starting downloading  process...")
                    start_downloading(obj)
                    print("Downloading completed successfully.")
                except Exception as e:
                    print(f"Error during Downloading : {e}")
 
                try:
                    print("Starting metadata extraction process...")
                    meta_data_main()
                    print("Metadata extraction completed successfully.")
                except Exception as e:
                    print(f"Error during metadata extraction: {e}")

                try:
                    print("Starting video hardcoding process...")
                    hardcode_all_videos()
                    print("Video hardcoding process completed successfully.")
                except Exception as e:
                    print(f"Error during video hardcoding process: {e}")

                try:
                    print("Starting upload of MKV files...")
                    upload_mkv_files()
                    print("MKV file upload completed successfully.")
                except Exception as e:
                    print(f"Error during MKV file upload: {e}")

                try:
                    print("Starting video splitting process...")
                    folder_name_lst = split_video_main()
                    print(f"Video splitting process completed. Processed folders: {folder_name_lst}")
                except Exception as e:
                    print(f"Error during video splitting process: {e}")

                try:
                    
                    print("Starting upload of hardcoded video folders...")
                    upload_hardcoded_videos_folders()
                    print("Hardcoded video folders uploaded successfully.")
                except Exception as e:
                    print(f"Error during upload of hardcoded video folders: {e}")
            except Exception as f:
                print("Error : ",e)
    else:   
        print("No data to process in the decrypted file.")
else:
    print(f"Error: File '{file_name}' not found.")
