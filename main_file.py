from final import main_fun
from mega import Mega
import os
import json
from decrypt import decrypt_json
from download_video import start_downloading
import re

# Get the password from the environment variable
key_pass = os.getenv("PASSWORD")
# Provide the correct file path (relative or absolute)
file_name = 'data_encrypted.json'

def sanitize_folder(title: str) -> str:
    # Remove content inside [] and () along with the brackets themselves
    sanitized_title = re.sub(r'[\[\(].*?[\]\)]', '', title)
    # Remove extra spaces from the start and end
    sanitized_title = sanitized_title.strip()
    return sanitized_title

import os
from mega import Mega

def check_files(folder_name):
    # Decrypt the JSON data
    file_name = os.path.join(os.getcwd(), file_name)
    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    
    # Login to Mega
    mega = Mega()
    m = mega.login(keys[0], keys[1])
    
    # Get all files
    all_files = m.get_files()
    
    total_size = 0  # Initialize variable to hold the total size
    folder_found = False  # Flag to check if folder is found
    folder_handle = None
    # Loop through all files
    for key, snippet in all_files.items():
        # Get the file name or folder name
        file_name = snippet['a']['h']
        
        # Check if the current item matches the folder name
        if file_name == folder_name and snippet['t'] == 1:
            folder_found = True
            folder_handle = 'key'
            # If it's a folder, we can get the contents and sum their sizes
            if 'f' in snippet:
                for file in snippet['f']:
                    # Check if the item is a file and not a subfolder
                    if 's' in file:
                        total_size += file['s']
                        
            # Once the size is calculated, break the loop
            break
    
    if folder_found and int(total_size)>0 and folder_handle:
        lst = []
        print(f"Total size of folder '{folder_name}' is {total_size / (1024 * 1024)} MB")
        for key,snippet in all_files.items():
            if snippet['p'] == folder_handle:
                file_name = snippet['a']['n']
                link = m.export(file_name)
                obj = {
                    'title':file_name,
                    'link':link
                }
                lst.append(obj)
    else:
        print(f"{folder_name} data not found in cloud..")
        return None


a_index = 146

# Check if the file exists before proceeding
if os.path.exists(file_name):

    data = decrypt_json(file_name, key_pass)

    files_present_flag = False
    
    if len(data) > 0:
        # Select a portion of the data (e.g., element at index 145 to 146)
        obj = data[a_index]
    if len(obj['data']) >= 2:
        folder_name = obj['data'][0]['title']
        folder_name = sanitize_folder(folder_name)
        lst_data = check_files(folder_name)    

        if lst_data and len(lst_data)>0:
            keys = os.getenv("M_TOKEN")
            keys = keys.split("_")
            mega =Mega() 

            keys[0] = keys[0].replace('6@','8@')
            m =  mega.login(keys[0],keys[1])

            for obj in lst_data:
                title = obj['title']
                link = obj['link']
                try:
                    m.download_url(link)
                except Exception as e:
                    print("Error failed to downlaod : ",e)
            files_present_flag = True
                
        else: 
            print(f" {30*'-'}\n{a_index} data not saved in cloud.. {30*'-'}\n")       
            # Call the main function with the selected data
            main_fun(obj,files_present_flag)
    else:
        print("No data to process in the decrypted file.")
else:
    print(f"Error: File '{file_name}' not found.")
