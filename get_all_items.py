import json
import requests
from bs4 import BeautifulSoup
import math
from decrypt import decrypt_json
import os
from mega import Mega
import time

# Example Usage
passphrase = os.getenv("PASSWORD")  # Replace with your passphrase
data = decrypt_json("encrypted_data.json", passphrase)

with open("output1.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

with open("output1.json", 'r', encoding='utf-8') as f:
    data = json.load(f) 
    l =len(data)//2
    l1=l*2
    data=data[l:l1]



def upload_tomega():
    mega = Mega()
    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    m = mega.login(keys[0], keys[1])
    try:
        m.upload("data1.json")
        print("File Uploaded Successfully.")
    except Exception as e:
        print("Error: Failed to upload:", e)

final_data = []

# Start tracking runtime
start_time = time.time()
time_limit = 5.5 * 60 * 60  # 5 hours 30 minutes in seconds

try:
    for index, entry_obj in enumerate(data):
        # Check if runtime exceeds the limit
        if time.time() - start_time > time_limit:
            print("Time limit exceeded. Stopping script and saving progress.")
            break
        
        obj_href = entry_obj['href']
        obj_title = entry_obj['title']
        obj_total_pages = entry_obj['total_items']

        if 'k' in obj_total_pages:
            num = str(obj_total_pages).split('k')[0]
            obj_total_pages = int(num) * 1000
        else:
            obj_total_pages = int(entry_obj['total_items'])

        obj_total_pages = math.ceil(obj_total_pages / 25)
        obj_data = []

        for obj_page in range(obj_total_pages):
            print(f"{index+1}/{len(data)} => {obj_page}/{obj_total_pages}")

            temp_link = f"{obj_href}/{obj_page+1}"
            response = requests.get(temp_link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                all_anchors = soup.select(".cover")
                for anchor in all_anchors:
                    # Safeguard in case there's no 'img' element inside the anchor
                    img = anchor.find("img")
                    img_src = img.get('data-src') if img and img.has_attr('data-src') else str(img)

                    # Create a dictionary for each anchor element
                    obj = {
                        "href": anchor.get('href'),  # Extract 'href' attribute
                        "img_source": img_src,       # Extract image source URL
                        "item_title": anchor.get_text(strip=True)  # Extract the title and clean up whitespace
                    }
                    obj_data.append(obj)

        final_obj = {
            obj_title: obj_data
        }
        final_data.append(final_obj)

except Exception as e:
    print("Error:", e)

finally:
    # Save the collected data to a JSON file
    with open("data1.json", 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)
    
    # Upload the file to Mega
    if os.path.exists("data1.json"):
        upload_tomega()
