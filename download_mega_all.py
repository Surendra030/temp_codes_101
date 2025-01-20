import os
from get_mega_instance import fetch_m

# from pymongo import MongoClient

# def upload_links_to_coll(lst):
#     # MongoDB Atlas connection URL
#     mongodb_url = os.getenv('MONGO_URL')
    
#     # Database and collection names
#     db_name = "temp_links_db"
#     coll_name = "temp_links_coll"
    
#     try:
#         # Connect to MongoDB Atlas
#         client = MongoClient(mongodb_url)
#         db = client[db_name]
#         collection = db[coll_name]
        
#         # Check if the collection is not empty and clear it
#         if collection.count_documents({}) > 0:
#             print(f"Clearing existing data from '{coll_name}'...")
#             collection.delete_many({})
#             print(f"Collection '{coll_name}' is now empty.")
        
#         # Upload the list of links
#         if lst:
#             print(f"Uploading {len(lst)} items to '{coll_name}'...")
#             # Ensure each item in the list is a dictionary
#             data_to_insert = [{"link": link} for link in lst] if isinstance(lst[0], str) else lst
#             collection.insert_many(data_to_insert)
#             print(f"Successfully uploaded {len(lst)} items to '{coll_name}'.")
#         else:
#             print("The provided list is empty. Nothing to upload.")
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
    
#     finally:
#         # Close the MongoDB connection
#         client.close()



# def get_links_from_coll():
#     # MongoDB Atlas connection URL
#     mongodb_url = os.getenv('MONGO_URL')
    
#     # Database and collection names
#     db_name = "temp_links_db"
#     coll_name = "temp_links_coll"
    
#     try:
#         # Connect to MongoDB Atlas
#         client = MongoClient(mongodb_url)
#         db = client[db_name]
#         collection = db[coll_name]
        
#         # Check if the collection is not empty
#         if collection.count_documents({}) > 0:
#             print(f"Collection '{coll_name}' is not empty. Retrieving data...")
#             # Fetch all documents and return as a list
#             data = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB `_id` field
#             print(f"Successfully retrieved {len(data)} items from '{coll_name}'.")
#             return data
#         else:
#             print(f"Collection '{coll_name}' is empty.")
#             return None  # Return an empty list if the collection is empty
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []
    
#     finally:
#         # Close the MongoDB connection
#         client.close()



def download_videos():
    download_videos_lst = []
    file_size = 0
    links_lst = []
    m  = fetch_m()
    all_files = m.get_files().items()





    for key,snippet in all_files:
        file_name = snippet['a']['n']

        if 'hardcoded.' in file_name:
            link = m.export(file_name)

            # Get the file size in bytes
            try:
                m.download_url(link)
                download_videos_lst.append(file_name)

                file_size = os.path.getsize(file_name)
                o = {
                    'link':link,
                    'file_name':file_name
                }
                links_lst.append(o)

                print(f"The size of '{file_name}' is {file_size} bytes.")
            except FileNotFoundError:
                print(f"The file '{file_name}' does not exist.")
    obj = {
        'total_file_size':file_size,
        'file_names_lst':download_videos_lst
    }

    # upload_links_to_coll(links_lst)

    return obj if len(download_videos_lst)>0 else None