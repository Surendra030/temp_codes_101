import re
import time
import os
import requests


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

            if total_size == 0:
                print("Warning: Unable to determine file size. Downloading without progress tracking...")
                with open(output_file, "wb") as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
                print(f"\nDownload of {title} complete. (Size: Unknown)")
                return output_file

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
                            f"({(downloaded_size / total_size) * 100:.2f}%)",
                            end="\r"
                        )

        if os.path.exists(output_file):
            print(f"\nDownload of {title} complete. (Size: {downloaded_size / size_divisor:.2f} {unit})")
            return output_file
        else:
            print(f"Error: File {output_file} not present after download.\nDirectory contents: {os.listdir()}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading {title}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
