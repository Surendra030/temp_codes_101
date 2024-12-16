from mega import Mega
import os

def get_files_with_links(parent_key: str):
    """
    Fetches all files under a given parent key in a Mega account and returns their names and shareable links.

    Args:
        parent_key (str): The parent key to filter files.

    Returns:
        list: A list of dictionaries containing file names and their shareable links.
    """
    # Get Mega account credentials from environment variable
    keys = os.getenv("M_TOKEN")
    if not keys:
        raise ValueError("Environment variable M_TOKEN is not set or empty.")
    
    keys = keys.split("_")
    if len(keys) != 2:
        raise ValueError("M_TOKEN should contain two parts separated by an underscore.")

    # Login to Mega
    mega = Mega()
    m = mega.login(keys[0], keys[1])

    # Fetch all files and filter by parent key
    all_files = m.get_files()
    links_lst = []

    for key, snippet in all_files.items():
        if snippet['p'] == parent_key:
            file_name = snippet['a']['n']
            link = m.export(file_name)
            links_lst.append({
                'file_name': file_name,
                'link': link
            })

    if not links_lst:
        print("No files found for the given parent key.")
    return links_lst[0:2]
