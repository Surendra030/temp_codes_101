import requests
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
    """
    Start downloading the file based on the provided object data using Selenium WebDriver.
    """
    title_splits = obj['title'].split("\n")
    url = obj['href']

    title = title_splits[0]
    file_size = title_splits[-1]
    file_name = sanitize_title(title)
    expected_size = convert_size_to_bytes(file_size)

    # Set up Selenium WebDriver with Chrome
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--headless")  # Optional: run headless for background operation
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")

    chromedriver_path = r"chromedriver"  # Path to your chromedriver
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Open the URL
    driver.get(url)
    time.sleep(3)  # Wait for the page to load (adjust if needed)

    # Handle Google Drive "confirmation required" process (if necessary)
    if "uc-warning-caption" in driver.page_source and 'No preview available' not in driver.page_source:
        print("File is too large to scan for viruses.")
        print("Initiating confirmation process to start the download...")
        # Find the form element using the correct method
        form = driver.find_element(By.ID, "download-form")

        # Submit the form to trigger the download
        form.submit()
  # Wait for confirmation to complete

        print("Confirmation successful. Starting the file download...")
    elif 'No preview available' in driver.page_source:
        print("The file is not downloadable. Google Drive reports 'No preview available'. Exiting the process.")
        driver.quit()
        exit()
    else:
        print("File can be downloaded directly without confirmation.")
        print("Starting the file download...")


    # Wait for the download to complete (You may need to customize this based on your setup)
    downloaded_size = 0
    last_check_time = time.time()
    while downloaded_size < expected_size:
        downloaded_size = os.path.getsize(file_name)
        current_time = time.time()
        if current_time - last_check_time >= 10:
            last_check_time = current_time
            print(f"Downloaded {downloaded_size / (1024 * 1024):.2f} MB out of {expected_size / (1024 * 1024):.2f} MB")
        time.sleep(5)  

    actual_size = os.path.getsize(file_name)
    if actual_size == expected_size:
        print(f"File downloaded successfully as '{file_name}' with the correct size.")
    else:
        print(f"Warning: File downloaded as '{file_name}' but the size ({actual_size / (1024 * 1024):.2f} MB) does not match the expected size ({expected_size / (1024 * 1024):.2f} MB).")

    driver.quit()
    return file_name





