from mega import Mega
from get_files_data import get_pdf_files_data
from paint_on_pdf import paint_white_area_on_pages
import os
import subprocess

def download_pdf_file(link, m):
    try:
        file_name = m.download_url(link)
        if file_name:
            return file_name  # Return the downloaded file name
        else:
            print("Failed to download the file.")
            return None
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

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
    m = mega.login(keys[0], keys[1])

    # Get PDF files data
    pdf_files_data = get_pdf_files_data()
    
    if not pdf_files_data:
        print("No PDF files found.")
        return
    
    print("Processing PDF files...")
    for item in pdf_files_data:
        for key, snippet in item.items():
            file_name = snippet['a']['n']
            link = m.export(file_name)
            parent_folder = snippet['p']

            downloaded_file = download_pdf_file(link, m)

            if downloaded_file:
                temp_name = file_name.split(".")
                paint_pdf_file_name = f"{temp_name[0]}_paint_.{temp_name[1]}"  # Specify the output file name
                painted_flag = paint_white_area_on_pages(downloaded_file,paint_pdf_file_name)
                
                

                output_file = f"{temp_name[0]}_paint_ocr_.{temp_name[1]}"  # Specify the output file name
                
                print(f"Running OCR on {downloaded_file}...")
                
                if painted_flag:
                    # Run OCR on the downloaded file
                    subprocess.run(['ocrmypdf', paint_pdf_file_name, output_file])
                    if os.path.exists(output_file):
                        upload_flag = upload_to_mega(output_file, parent_folder, m)
                        if upload_flag:
                            os.remove(output_file)
                            if os.path.exists(downloaded_file):
                                os.remove(downloaded_file)
                            print("File successfully uploaded to Cloud")
                else:
                    print("Output file not exits.")
                    print(os.listdir())

# Call the processing function
process_pdf_files()
