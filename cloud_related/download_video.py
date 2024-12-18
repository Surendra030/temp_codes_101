import os
from mega import Mega
import time
def download_file_from_link(link: str) -> bool:
    # Initialize Mega instance and login
    mega = Mega()
    keys  = os.getenv("M_TOKEN")
    keys = keys.split("_")    
    m = mega.login(keys[0], keys[1])

    print("File downloading started.")
    # Download the file using the link
    try:
        file_name = m.download_url(link)  # This should return the file path
        print("File downloaded successfully.")
        return file_name  # Ensure it returns the actual file path
    except Exception as e:
        print("Error occurred while downloading file.", e)
        return None 
   