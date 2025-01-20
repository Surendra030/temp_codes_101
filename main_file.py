from mega import Mega
import os
import json
import time
import traceback

from decrypt import decrypt_json
from upload_before_coded import upload_mkv_files
from download_video import start_downloading
from get_meta_data import meta_data_main
from hardcode_videos import hardcode_all_videos
from upload_videos import upload_hardcoded_videos_folders
from split_video import split_video_main
from download_mega_all import download_videos
from get_mega_instance import fetch_m

# Get the password from the environment variable

key_pass = os.getenv("PASSWORD", "noText!")

# Provide the correct file path (relative or absolute)
file_name = 'data_encrypted.json'

a_index = 141

def upload_links_json():

    m = fetch_m()

    files_lst = []

    all_files = m.get_files().items()

    for key,snippet in all_files:
        file_name = snippet['a']['n']
        if '.zip' in file_name:
            link = m.export(file_name)
            files_lst.append(link)

    json_file = 'videos_links.json'
    with open(json_file,'w')as f:
        json.dump(files_lst,f,indent=4)
    try:
            
        m.upload(json_file)
    except Exception as e:
        print("Error : ",e)

# upload_links_json()


# Check if the file exists before proceeding
if os.path.exists(file_name):

    data = decrypt_json(file_name, key_pass)
    names_size_lst = {}
    already_files_present = True
    folder_name_lst = []

    if len(data) > 0:

        main_obj = data[a_index]

        data  = main_obj['data'][1:]
        data = data if len(data)<=12 else data[:12]
        
        for obj in data :

            if True:
                try:
                    try:
                        print(f"{30 * '-'}")

                        print("Starting downloading process...")
                        start_time = time.time()
                        start_downloading(obj)
                        elapsed_time = time.time() - start_time
                        print(f"Downloading completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                    except Exception as e:
                        traceback.print_exc()
                        print(f"Error during downloading: {e}")


                    if already_files_present:
                        try:
                            print(f"{30 * '-'}")
                            print("Starting metadata extraction process...")
                            start_time = time.time()
                            meta_data_main()
                            elapsed_time = time.time() - start_time
                            print(f"Metadata extraction completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                        except Exception as e:
                            traceback.print_exc()
                            print(f"Error during metadata extraction: {e}")

                        try:
                            print(f"{30 * '-'}")
                            print("Starting video hardcoding process...")
                            start_time = time.time()
                            hardcode_all_videos()
                            elapsed_time = time.time() - start_time
                            print(f"Video hardcoding process completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                        except Exception as e:
                            traceback.print_exc()
                            print(f"Error during video hardcoding process: {e}")
                        try:
                            print(f"{30 * '-'}")
                            print("Starting upload of MKV files...")
                            start_time = time.time()
                            upload_mkv_files()
                            elapsed_time = time.time() - start_time
                            print(f"MKV file upload completed successfully. Time taken: {elapsed_time:.2f} seconds.")
                        except Exception as e:
                            traceback.print_exc()
                            print(f"Error during MKV file upload: {e}")
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
                        traceback.print_exc()
                        print(f"Error during video splitting process: {e}")

                    try:
                        print(f"{30 * '-'}")
                        print("Starting upload of hardcoded video folders...")
                        start_time = time.time()
                        upload_hardcoded_videos_folders()
                        elapsed_time = time.time() - start_time
                        print(f"Hardcoded video folders uploaded successfully. Time taken: {elapsed_time:.2f} seconds.")
                    except Exception as e:
                        traceback.print_exc()
                        print(f"Error during upload of hardcoded video folders: {e}")

                except Exception as f:
                    traceback.print_exc()
                    print(f"Error: {f}")
    else:
        print("No data to process in the decrypted file.")
else:
    print(f"Error: File '{file_name}' not found.")
