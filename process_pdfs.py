from mega import Mega
from get_files_data import get_pdf_files_data
from mega import Mega
import os
import subprocess

def download_pdf_file(link,m):
    
    file_name = m.download_url(link)
    if file_name:
        return True
    else: False

def upload_to_mega(file, parent_handle, m):
    
    try:
        print(f"Uploading file: {file} to parent handle: {parent_handle}")
        m.upload(file, parent_handle)
        print(f"Upload successful for file: {file}")
        return True
    except Exception as e:
        print(f"Error: Failed to upload file '{file}'. Exception: {e}")
        return False

def process_pdf_files():

    mega = Mega()
    keys = os.getenv("M_TOKEN")
    keys = keys.split("_")
    m = mega.login(keys[0],keys[1])

    # Call the function to get PDF file data
    pdf_files_data = get_pdf_files_data()
    
    if not pdf_files_data:
        print("No PDF files found.")
        return
    
    print("Processing PDF files...")
    for item in pdf_files_data:
        for key, snippet in item.items():
            # Extracting the key and snippet data
            file_name = snippet['a']['n']
            link = m.export(file_name)
            parent_folder = snippet['p']

            download_flag = download_pdf_file(link,m)

            if download_flag:
                    temp_name = file_name.split(".")

                    output_file = f"{temp_name[0]}_ocr_.{temp_name[1]}"  # Specify the output file name
                    print(f"Running OCR on {file_name}...")
                    
                    # Using subprocess to run the ocrmypdf command
                    subprocess.run(['ocrmypdf', file_name, output_file])
                    if os.path.exists(output_file):
                        upload_flag = upload_to_mega(output_file,parent_folder,m)
                        if upload_flag : print("File Sucessfully uploaded to Cloud")

# Call the processing function
process_pdf_files()
