import os
from get_mega_instance import fetch_m


def download_videos():
    download_videos_lst = []
    file_size = 0

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
                print(f"The size of '{file_name}' is {file_size} bytes.")
            except FileNotFoundError:
                print(f"The file '{file_name}' does not exist.")
    obj = {
        'total_file_size':file_size,
        'file_names_lst':download_videos_lst
    }
    return obj if len(download_videos_lst)>0 else None