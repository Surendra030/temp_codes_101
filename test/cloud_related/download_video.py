import os
import shutil
from mega import Mega

def download_file_from_link(link: str) -> bool:
    # Initialize Mega instance and login
    mega = Mega()
    keys = os.getenv("M_TOKEN").split("_")
    m = mega.login(keys[0], keys[1])

    # Download the file using the link
    file_obj = m.download_url(link)
    if file_obj:
        # Extract the file name from the file object
        file_name = file_obj.name

        # Define the destination folder inside 'temp/videos'
        temp_folder = "videos"
        os.makedirs(temp_folder, exist_ok=True)  # Create 'temp/videos' if it doesn't exist

        # Define the destination path for the file
        destination_path = os.path.join(temp_folder, file_name)

        # Move the downloaded file to the videos folder
        shutil.move(file_name, destination_path)
        print(f"File moved to: {destination_path}")

        return destination_path

    return False
