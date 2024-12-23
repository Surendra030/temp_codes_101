import requests
from bs4 import BeautifulSoup
import json
import time
import os
from mega import Mega
from concurrent.futures import ThreadPoolExecutor

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
    
    # Upload to Mega (if needed)
    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    mega = Mega()
    m = mega.login(keys[0], keys[1])
    try:
        m.upload(filename)
    except Exception as e:
        print("Error: Failed to upload file.", e)

def fetch_links_for_pages(start_page, end_page, base_url):
    all_links = []
    for page in range(start_page, end_page + 1):
        url = base_url.format(page)
        links = extract_links(url)
        obj = {
            'page_num': page,
            'Links_data': links
        }
        all_links.append(obj)
        print(f"Fetched links for page {page}")
        time.sleep(1)  # Add a delay to avoid hitting the server too fast
    return all_links

def main():
    start_page = 1
    end_page = 50000  # For example, fetching 10 pages
    base_url = "https://e-hentai.org/?next={}"
    output_file = f"output_{end_page}.json"
    
    all_links = []
    
    # Start the timer to track execution time
    start_time = time.time()
    max_runtime = 5.5 * 60 * 60  # 5.5 hours in seconds
    
    # Using ThreadPoolExecutor to fetch links for 5 pages at a time
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        
        # Iterate through pages in chunks (100 at a time)
        for page_start in range(start_page, end_page + 1, 100):
            page_end = min(page_start + 4, end_page)  # Make sure we don't go beyond the end_page
            
            # Check if time exceeded 5.5 hours
            elapsed_time = time.time() - start_time
            if elapsed_time > max_runtime:
                print("Time limit exceeded. Saving collected data...")
                save_to_json(all_links, output_file)
                return  # Stop execution
            
            futures.append(executor.submit(fetch_links_for_pages, page_start, page_end, base_url))
        
        # Wait for all threads to complete and gather results
        for future in futures:
            result = future.result()
            all_links.extend(result)  # Add the result to the main list
    
    # Final saving of data to the file and cloud
    save_to_json(all_links, output_file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Saving collected data before exiting...")
        save_to_json([], "error_output.json")  # Optionally save error state
