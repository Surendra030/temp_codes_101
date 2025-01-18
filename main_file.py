from final import main_fun
from mega import Mega
import os
import json
from decrypt import decrypt_json

# Get the password from the environment variable
key_pass = os.getenv("PASSWORD")
# Provide the correct file path (relative or absolute)
file_name = 'data_encrypted.json'

# Check if the file exists before proceeding
if os.path.exists(file_name):
    # Decrypt the JSON data
    file_name = os.path.join(os.getcwd(),file_name)
    data = decrypt_json(file_name, key_pass)

    if len(data) > 0:
        # Select a portion of the data (e.g., element at index 145 to 146)
        obj = data[145:146]

        # Call the main function with the selected data
        main_fun(obj[0])
    else:
        print("No data to process in the decrypted file.")
else:
    print(f"Error: File '{file_name}' not found.")
