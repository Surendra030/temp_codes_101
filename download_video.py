from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import re
import time
import os
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)
    return sanitized_title

def download_large_file(download_url, file_id, title):
    driver = webdriver.Chrome()

    try:
        # Open the download URL
        driver.get(download_url)

        # Check if "uc-warning-caption" exists
        if driver.page_source.find("uc-warning-caption") != -1:
            print("File is too large to scan for viruses.")
            print("Submitting the form to start the download...")

            # Submit the form
            form = driver.find_element(By.ID, "download-form")
            form.submit()

            # Extract title and expected size from provided title
            title_splits = title.split(" ")
            file_size = title_splits[-1]
            sanitized_title = sanitize_title(" ".join(title_splits[:-1]))
            file_name = f"{sanitized_title}.download"
            expected_size = convert_size_to_bytes(file_size)

            # Wait and monitor the file size
            while True:
                if os.path.exists(file_name):
                    actual_size = os.path.getsize(file_name)
                    print(f"Downloaded size: {actual_size / (1024 * 1024):.2f} MB out of {expected_size / (1024 * 1024):.2f} MB")
                    
                    if abs(actual_size - expected_size) <= (1024 * 1024):  # Within 1 MB
                        print("File size matches the expected size.")
                        time.sleep(5)  # Wait an additional 5 seconds
                        break
                else:
                    print("Waiting for the file to appear...")
                
                time.sleep(10)  # Check every 10 seconds

            # Close the browser
            driver.quit()

            # Rename the file and return
            os.rename(file_name, f"{sanitized_title}.zip")
            print(f"File downloaded successfully as '{sanitized_title}.zip'.")
            return f"{sanitized_title}.zip"

        else:
            print("File can be downloaded directly without confirmation.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None
