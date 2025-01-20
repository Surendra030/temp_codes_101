from mega import Mega
import os
import json
import time
from decrypt import decrypt_json
from upload_before_coded import upload_mkv_files
from download_video import start_downloading
from get_meta_data import meta_data_main
from hardcode_videos import hardcode_all_videos
from upload_videos import upload_hardcoded_videos_folders, deleted_all_videos
from split_video import split_video_main
from download_mega_all import download_videos

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
    names_size_lst = {}
    already_files_present = []
    folder_name_lst = []
    
    if len(data) > 0:
        print(f"Decrypted data successfully. Processing data at index {a_index}...")
        main_obj = data[a_index]
 
        try:

            print("checking cloud  videos..")
            names_size_lst  = download_videos()
            print("Checking completed successfully.")

        except Exception as e:
            print(f"Error during Downloading : {e}")
        files_names_lst = names_size_lst['file_names_lst']

        print(os.listdir())


        for obj in main_obj['data'][1:]:
            for file_name_present in files_names_lst:
                try:
                    # try:
                    #     print(f"{30 * '-'}")

                    #     print("Starting downloading process...")
                    #     start_time = time.time()
                    #     already_files_present = start_downloading(obj, file_name_present)
                    #     elapsed_time = time.time() - start_time
                    #     print(f"Downloading completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                    # except Exception as e:
                    #     print(f"Error during downloading: {e}")

                    if already_files_present == False:
                        try:
                            print(f"{30 * '-'}")
                            print("Starting metadata extraction process...")
                            start_time = time.time()
                            meta_data_main()
                            elapsed_time = time.time() - start_time
                            print(f"Metadata extraction completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                        except Exception as e:
                            print(f"Error during metadata extraction: {e}")

                        try:
                            print(f"{30 * '-'}")
                            print("Starting video hardcoding process...")
                            start_time = time.time()
                            hardcode_all_videos()
                            elapsed_time = time.time() - start_time
                            print(f"Video hardcoding process completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                        except Exception as e:
                            print(f"Error during video hardcoding process: {e}")

                        try:
                            print(f"{30 * '-'}")
                            print("Starting upload of MKV files...")
                            start_time = time.time()
                            upload_mkv_files()
                            elapsed_time = time.time() - start_time
                            print(f"MKV file upload completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                        except Exception as e:
                            print(f"Error during MKV file upload: {e}")
                        print(f"{30 * '-'}")
                    else:
                        print("Video already hardcoded.")

                    try:
                        print(f"{30 * '-'}")
                        print("Starting video splitting process...")
                        start_time = time.time()
                        split_video_main()
                        elapsed_time = time.time() - start_time
                        print(f"Video splitting process completed. Processed folders: {folder_name_lst}. Time taken: {elapsed_time:.2f} seconds.")
                    except Exception as e:
                        print(f"Error during video splitting process: {e}")

                    try:
                        print(f"{30 * '-'}")
                        print("Starting upload of hardcoded video folders...")
                        start_time = time.time()
                        upload_hardcoded_videos_folders()
                        elapsed_time = time.time() - start_time
                        print(f"Hardcoded video folders uploaded successfully. Time taken: {elapsed_time:.2f} seconds.")
                    except Exception as e:
                        print(f"Error during upload of hardcoded video folders: {e}")

                except Exception as f:
                    print(f"Error: {f}")

            
    
    
    
    
    
    
    
    
    
    
    
    else:   
        print("No data to process in the decrypted file.")
else:
    print(f"Error: File '{file_name}' not found.")
