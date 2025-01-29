import shutil
import json
import time
from moviepy.editor import VideoFileClip
import os
from get_mega_instance import fetch_df,fetch_m
def process_video_file(video_path: str, filename: str, part_duration: int = 13 * 60) -> list:
    """
    Splits a video into 13-minute parts and returns a list of dictionaries containing 
    the video part path and name.

    :param video_path: The path of the video file to split.
    :param filename: The base filename of the video.
    :param part_duration: Duration of each video part in seconds (default is 13 minutes).
    :return: List of dictionaries containing video part paths and names.
    """
    # Load the video
    video = VideoFileClip(video_path)
    
    # Get the video duration in seconds
    video_duration = video.duration  # Duration in seconds
    
    # Number of parts to split the video into
    num_parts = int(video_duration // part_duration) + (1 if video_duration % part_duration != 0 else 0)
    
    # Create a temporary folder for the video parts if it doesn't exist
    temp_folder = r"D:\files\practice\project_youtube_automate\light_novel_pdf_videos"
    os.makedirs(temp_folder, exist_ok=True)
    
    video_parts = []
    
    # Split the video into parts
    for i in range(num_parts):
        start_time = i * part_duration
        end_time = min((i + 1) * part_duration, video_duration)
        
        # Create the video part using the subclip method
        video_part = video.subclip(start_time, end_time)
        
        # Name the video part (e.g., video_part_1, video_part_2, etc.)
        temp_name = f"{filename}_part_{i + 1}.mp4"
        temp_path = os.path.join(temp_folder, temp_name)
        # Write the part to the temp folder
        video_part.write_videofile(temp_path, codec="libx264", audio_codec="aac")
        
        # Add the part to the video_parts list
        video_parts.append({
            'videopath': temp_path,
            'video_name': temp_name
        })
        time.sleep(5)

    # Close the video file
    video.close()
    
    return video_parts




m = fetch_m()
all_files = m.get_files().items()
try:
        
    for key,snippet in all_files:
        try:
            
            file_name = snippet['a']['n']
            if '.mp4' in file_name:
                file = m.find(file_name)
                m.download(file)
        except Exception as e:
            print("Error failed to download..")
            
except Exception as e:
    print("Errro 77 : ",e)        



files_temp = [f for f in os.listdir() if str(f).endswith(".mp4")]
start = os.getenv("START")
start = int(start)
end = start + 100
light_novel_names = set()
file_n = 'light_novel_names.json'
try:
        
    for index,video_path in enumerate(files_temp,start=1):            
            
        print(f"{index}/{len(files_temp)}")
        video_path = f"{video_path}"
        
        temp_name = file_name.split(".")[0]

        process_video_file(video_path,temp_name)
        light_novel_names.add(temp_name)

finally:
    m = fetch_df("06")
    try:
        folder_name = f"{end}_videos"
        os.makedirs(folder_name, exist_ok=True)

        temp_lst = [f for f in os.listdir() if f.endswith(".mp4")]
        for tf in temp_lst:
            shutil.move(tf, folder_name)

        # Create a ZIP file from the folder
        zip_filename = f"{folder_name}.zip"
        shutil.make_archive(folder_name, 'zip', folder_name)
        try:
            if os.path.exists(zip_filename):
                m.upload(zip_filename)
        except Exception as e:
            print("Error 115 :",e)
        
    except Exception as e:
        print(f"118 Error while handling files: {e}")

    try:
        with open(file_n, 'w', encoding='utf-8') as f:
            json.dump(light_novel_names, f, indent=4)
        if os.path.exists(file_n):
            m.upload(file_n)
    except Exception as e:
        print(f" 126 Error while writing JSON file: {e}")
    