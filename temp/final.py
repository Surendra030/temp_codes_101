from download_video import start_downloading
from get_audio_sub import get_meta_data
import os
import subprocess
from mega import Mega

def hardcode_subtitles(video_path, subtitle_path, output_path):
    # Check if the input files exist
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    if not os.path.exists(subtitle_path):
        print(f"Error: Subtitle file '{subtitle_path}' not found.")
        return

    # Path to the locally stored ffmpeg binary (relative path to your repository)
    ffmpeg_path = '../ffmpeg/ffmpeg'  # Adjust this path based on where ffmpeg is stored in your repo
    ffmpeg_path = os.path.join(os.getcwd(),ffmpeg_path)
    # Ensure ffmpeg binary exists at the specified path
    if not os.path.exists(ffmpeg_path):
        print(f"Error: ffmpeg binary not found at '{ffmpeg_path}'.")
        return
    
    # Build the ffmpeg command
    cmd = [
        ffmpeg_path,               # Use local ffmpeg binary
        "-i", video_path,          # Input video file
        "-i", subtitle_path,       # Input subtitle file
        "-c:v", "libx264",         # Video codec
        "-c:a", "copy",            # Audio codec (copy audio without re-encoding)
        "-c:s", "mov_text",        # Subtitle codec (to merge subtitles)
        output_path                # Output file
    ]
    
    # Execute the command
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
    # Set paths to the files
    print(os.listdir(),"\n",os.getcwd())

    subtitle_file = 'subtitle_1.ass'
    output_file = 'output_file.mkv'

    # Call the function
    hardcode_subtitles(file_name, subtitle_file, output_file)

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