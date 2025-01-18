
import re
import time
import os

import requests
def convert_size_to_bytes(size_str):
    """Convert size string (e.g., '10 MB') to bytes."""
    size_str = size_str.upper().strip()
    size, unit = size_str.split()
    size = float(size)
    unit = unit.strip()

    if unit == "KB":
        return int(size * 1024)
    elif unit == "MB":
        return int(size * 1024 * 1024)
    elif unit == "GB":
        return int(size * 1024 * 1024 * 1024)
    else:
        raise ValueError("Unsupported size unit")

def sanitize_title(title):
    """
    Sanitize the title to create a valid filename by removing unwanted characters.
    """
    file_name = re.sub(r'[\\/*?:"<>|]', "", title)
    return file_name


def start_downloading(obj, chunk_size=1024 * 1024, timeout=10):  # Chunk size = 1 MB
    try:
        # Extract title and URL from the object
        title_splits = obj['title'].split("\n")
        url = obj['href']
        title = sanitize_title(title_splits[0])
        output_file = title
        print(f"Starting download for: {title} ({url})")
        
        with requests.get(url, stream=True, timeout=timeout) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded_size = 0

            # Determine the display unit (MB or GB)
            if total_size < 1024 * 1024 * 1024:  # Less than 1 GB
                unit = "MB"
                size_divisor = 1024 * 1024
            else:
                unit = "GB"
                size_divisor = 1024 * 1024 * 1024

            total_size_display = total_size / size_divisor

            with open(output_file, "wb") as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:  # Filter out keep-alive chunks
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        downloaded_size_display = downloaded_size / size_divisor

                        # Show progress in the correct unit
                        print(
                            f"Downloaded {downloaded_size_display:.2f}/{total_size_display:.2f} {unit} "
                            f"({(downloaded_size/total_size)*100:.2f}%)",
                            end="\r"
                        )
        
        if os.path.exists(output_file):
            print("\nDownload complete.")
            return output_file
        else:
            print(f"{output_file} not present \n{os.listdir()}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading {title}: {e}")
