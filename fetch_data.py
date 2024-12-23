import requests
from bs4 import BeautifulSoup
import json
import time
import os
from mega import Mega
def extract_links(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {url}, Status Code: {response.status_code}")
        return []
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all <a> elements
    anchors = soup.find_all("a")
    print(f"Total <a> elements found: {len(anchors)}")
    
    # Filter <a> elements based on href containing '.org/g/'
    filtered_links = []
    for anchor in anchors:
        href = anchor.get("href", "")
        text = anchor.get_text(strip=True)
        if ".org/g/" in href:
            filtered_links.append({"href": href, "text": text})
    
    return filtered_links

def save_to_json(data, filename):
    # Save the data to a JSON file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")
    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    mega = Mega()
    m  = mega.login(keys[0],keys[1])
    try:
        m.upload(filename)
    except Exception as e:
        print("Error failed to upload file.")

# Main logic
if __name__ == "__main__":
    start_page = 3_000_001
    # end_page = 3168234
    end_page = 3168234

    base_url = "https://e-hentai.org/?next={}"
    output_file = f"output{end_page}.json"
    
    # Store all fetched links
    all_links = []

    try:
        for page in range(start_page, end_page + 1):
            url = base_url.format(page)
            
            # Extract links from the current page
            links = extract_links(url)
            obj = {
                'page_num' : page,
                'Links_data':links
            }
            all_links.extend(obj)  # Append the links to the main list
            
            # Periodically save progress every 100 pages
                
            # Delay to avoid overloading the server
              # Adjust delay as needed
        
            print(f"progress up to page{page}")
            time.sleep(1)
        save_to_json(all_links, output_file)
            
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Save data collected so far
        print("Saving fetched data before exiting...")
        save_to_json(all_links, output_file)
