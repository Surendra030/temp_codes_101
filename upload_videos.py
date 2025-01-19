from mega import Mega
import os
import json
from get_mega_instance import fetch_m

m = fetch_m()


def deleted_all_videos(do_not_remove_final=True,do_not_remove=True):
    m = fetch_m()


    all_files = m.get_files().items()
    for key,snippet in all_files:
        file_folder = snippet['t']
        if file_folder == 0:
            if('do_not_remove' not in snippet['a']['n']) and do_not_remove:

                if('do_not_remove_final' not in snippet['a']['n']) and do_not_remove_final:

                    m.delete(key)
            elif ('do_not_remove' in snippet['a']['n']) and 'do_not_remove_final' not in snippet['a']['n'] and do_not_remove == False:
                m.delete(key)
    print("All files are deleted sucessfully..")



def upload_hardcoded_videos_folders():
    try:
        deleted_all_videos(do_not_remove=False)
        files = os.listdir()
        folder_name_lst = []
        for file in files:
            if 'do_not_remove_hardcoded_videos' in file:
                folder_name_lst.append(file)

        for folder_name in folder_name_lst:
            print(folder_name)

            try:
                # Create folder and get its handle
                file = m.create_folder(folder_name)
                if folder_name not in file:
                    raise KeyError(f"Folder '{folder_name}' creation failed.")
                f_h = file[folder_name]
                files_in_folder = os.listdir(folder_name)
                # Iterate through files in the folder and upload
                for index,file_name in enumerate(files_in_folder):

                    full_path = os.path.join(folder_name, file_name)
                    
                    try:
                        m.upload(full_path, f_h)

                        os.remove(full_path)
                        print(f"file : {index} uploaded sucessfully.. ")
                    except Exception as e:
                        print(f"Error uploading/removing file '{file_name}': {e}")
            except Exception as e:
                print(f"Error processing folder '{folder_name}': {e}")
        
        print("Hardcoded video folders uploaded successfully.")
    except Exception as e:
        print(f"Error during upload of hardcoded video folders: {e}")

