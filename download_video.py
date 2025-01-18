import requests
import re
import time
import os

def sanitize_title(title):
    """
    Sanitize the title to create a valid filename by removing unwanted characters.
    """
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)
    sanitized_title = re.sub(r'[\[\(].*?[\]\)]', '', title)
    sanitized_title = sanitized_title.strip()

    return sanitized_title

def convert_size_to_bytes(size_str: str) -> int:
    size_str = size_str.strip()  # Strip any extra spaces
    parts = size_str.split()
    
    if len(parts) == 2:
        size, unit = parts
    else:
        print(f"Unexpected format for size string: {size_str}")
        return 0  # or handle accordingly
    
    size = float(size)
    if unit.lower() == 'mb':
        return int(size * 1024 * 1024)
    elif unit.lower() == 'gb':
        return int(size * 1024 * 1024 * 1024)
    # Add more units as necessary
    else:
        print(f"Unknown unit: {unit}")
        return 0


def start_downloading(obj):
    # Example usage


    """
    Start downloading the file based on the provided object data.
    """
    title_splits = obj['title'].split("\n")
    url = obj['href']

    title = title_splits[0]
    file_size = title_splits[-1]
    file_name = sanitize_title(title)
    expected_size = convert_size_to_bytes(file_size)

    file_id = re.search(r'/d/([a-zA-Z0-9_-]+)', url).group(1)
    download_url = f"https://drive.google.com/uc?id={file_id}&export=download"

    response = requests.get(download_url, allow_redirects=True)

    if "uc-warning-caption" in response.text and 'No preview available' not in response.text:
        print("File is too large to scan for viruses.")
        print("Initiating confirmation process to start the download...")

        confirm_url = "https://drive.usercontent.google.com/download"
        params = {
            'id': file_id,
            'export': 'download',
            'confirm': 't',
        }

        print(f"Sending confirmation request to url")
        download_response = requests.get(confirm_url, params=params, stream=True)

        if download_response.status_code == 200:
            print("Confirmation successful. Starting the file download...")
            with open(file_name, "wb") as file:
                downloaded_size = 0
                last_check_time = time.time()
                for chunk in download_response.iter_content(chunk_size=1048576):  # 1 MB chunks
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    # Check every 10 seconds
                    current_time = time.time()
                    if current_time - last_check_time >= 10:
                        last_check_time = current_time
                        print(f"Downloaded {downloaded_size / (1024 * 1024):.2f} MB out of {expected_size / (1024 * 1024):.2f} MB")

            # Verify if the download size matches the expected size
            actual_size = os.path.getsize(file_name)
            if actual_size == expected_size:
                print(f"File downloaded successfully as '{file_name}' with the correct size.")
            else:
                print(f"Warning: File downloaded as '{file_name}' but the size ({actual_size / (1024 * 1024):.2f} MB) does not match the expected size ({expected_size / (1024 * 1024):.2f} MB).")
        else:
            print(f"Failed to download the file after confirmation. Status code: {download_response.status_code}")
            print("Please check the file ID and your network connection.")

    elif 'No preview available' in response.text:
        print("The file is not downloadable. Google Drive reports 'No preview available'. Exiting the process.")
        exit()

    else:
        print("File can be downloaded directly without confirmation.")
        print("Starting the file download...")
        with open(file_name, "wb") as file:
            downloaded_size = 0
            last_check_time = time.time()
            for chunk in response.iter_content(chunk_size=1048576):
                file.write(chunk)
                downloaded_size += len(chunk)

                # Check every 10 seconds
                current_time = time.time()
                if current_time - last_check_time >= 10:
                    last_check_time = current_time
                    print(f"Downloaded {downloaded_size / (1024 * 1024):.2f} MB out of {expected_size / (1024 * 1024):.2f} MB")

        actual_size = os.path.getsize(file_name)
        if actual_size == expected_size:
            print(f"File downloaded successfully as '{file_name}' with the correct size.")
            
            return file_name
        else:
            print(f"Warning: File downloaded as '{file_name}' but the size ({actual_size / (1024 * 1024):.2f} MB) does not match the expected size ({expected_size / (1024 * 1024):.2f} MB).")
            return file_name






