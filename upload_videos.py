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
        
        print(f'{30*"*"}')
        files_lst = os.listdir()
        for index,i in enumerate(files_lst,start=1):
            if index % 4 ==0:
                print(i,end='\n')
                continue

            print(i,end='\t')
        print(f'{30*"*"}')



        for file in files_lst:

            if '.zip' in file:
                                    
                try:
                    m.upload(file)

                    os.remove(file)
                    print(f"file : {file} uploaded sucessfully.. ")
                except Exception as e:
                    print(f"Error uploading/removing file '{file}': {e}")
 
    except Exception as e:
        print(f"Error during upload of hardcoded video folders: {e}")

