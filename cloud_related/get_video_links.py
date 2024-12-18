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
    keys = 'afg154006@gmail.com_megaMac02335!'
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

    for index, (key, snippet) in enumerate(all_files.items(), start=1):
    # Clear the previous output
        os.system("cls" if os.name == "nt" else "clear")

        # Print the current processing message
        print(f"Processing snippet {len(all_files)} {index}: {snippet['a']['n']}")

        # Process the snippet
        if snippet['p'] == parent_key:
            file_name = snippet['a']['n']
            link = m.export(file_name)
            links_lst.append({
                'file_name': file_name,
                'link': link
            })

        # Optional: Provide feedback once the snippet has been processed
        print(f"Snippet {index} processing completed!")

    if  links_lst:
        print(f"files found for the given parent key.{len(links_lst)}")
    else:
        print("No files found for the given parent key.")
    return links_lst[3:11]
