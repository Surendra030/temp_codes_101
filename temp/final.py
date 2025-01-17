from download_video import start_downloading
from get_audio_sub import get_meta_data
import os
import subprocess
from mega import Mega

import os
import subprocess

def convert_ass_to_srt(ass_path, srt_path):
    """
    Converts an .ass subtitle file to .srt format using ffmpeg.
    """
    cmd = [
        'ffmpeg',               # Use local ffmpeg binary
        '-i', ass_path,         # Input .ass subtitle file
        srt_path                # Output .srt subtitle file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully converted {ass_path} to {srt_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during subtitle conversion: {e}")
        return False
    return True

def hardcode_subtitles(video_path, subtitle_path, output_path):
    """
    Hardcodes subtitles into a video by first converting the .ass file to .srt
    and then using the .srt file to merge the subtitles into the video.
    """
    # Check if the input video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    
    # Check if the subtitle file exists
    if not os.path.exists(subtitle_path):
        print(f"Error: Subtitle file '{subtitle_path}' not found.")
        return

    # Generate the output SRT path (same as input subtitle path, but with .srt extension)
    srt_subtitle_path = subtitle_path.rsplit('.', 1)[0] + '.srt'
    
    # Step 1: Convert .ass to .srt
    if not convert_ass_to_srt(subtitle_path, srt_subtitle_path):
        print("Subtitle conversion failed. Aborting.")
        return
    
    # Step 2: Build the ffmpeg command to hardcode subtitles into the video
    cmd = [
        'ffmpeg',               # Use local ffmpeg binary
        "-i", video_path,       # Input video file
        "-i", srt_subtitle_path,  # Input subtitle file (converted .srt)
        "-c:v", "libx264",      # Video codec (H.264)
        "-c:a", "copy",         # Audio codec (copy without re-encoding)
        "-c:s", "mov_text",     # Subtitle codec (to merge subtitles)
        output_path             # Output file with hardcoded subtitles
    ]
    
    # Execute the command to hardcode subtitles
    try:
        subprocess.run(cmd, check=True)
        print(f"Subtitles have been successfully hardcoded into the video. Output saved as: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg execution: {e}")


obj = {
        "title": "file.mkv\nOwner hidden\n8 May 2022\n357.8 MB",
        "href": "https://drive.google.com/file/d/1fDzOWm6YBpqRetZIWopAy962ADf5r6nv/view?usp=drive_link"
    }

file_name = start_downloading(obj)
file_name = 'file.mkv'

if file_name and os.path.exists(file_name):
    flag_result =  get_meta_data(file_name)
    
    if flag_result:
            

        subtitle_file = 'subtitle_1.ass'
        output_file = 'output_file.mkv'

        try:
        # Call the function
            hardcode_subtitles(file_name, subtitle_file, output_file)
        except Exception as e:
            print("Error failed to execute : ",e)
        print(os.listdir())
        if os.path.exists(output_file):
            
            mega = Mega()
            keys = os.getenv('M_TOKEN')
            keys = keys.split("_")

            try:

                m  = mega.login(keys[0],keys[1])
                m.upload(output_file)

            except Exception as e:
                print("Error failed to upload file : ",e)
else:print(f"{file_name} not found..")