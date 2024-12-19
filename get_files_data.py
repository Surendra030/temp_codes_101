from mega import Mega
import os

def get_pdf_files_data():
    mega = Mega()
    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    m = mega.login(keys[0],keys[1])
    all_files = m.get_files()
    temp_lst = []
    l = len(all_files)
    c = 0
    for key,snippet in all_files.items():
        c+=1
        print(f"{c}/{l}")
        file_name = snippet['a']['n']
        if '.pdf' in file_name and 'compress.pdf' not in file_name and 'ocr' not in file_name:
            temp_lst.append({
                key:snippet
            }) 
    
    if temp_lst:
        return temp_lst
    else: return None