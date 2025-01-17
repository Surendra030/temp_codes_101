from download_video import start_downloading
from get_audio_sub import get_meta_data
from split_video import split_video

import os
import subprocess
from mega import Mega
import re


def convert_time(ass_time):
    """Convert ASS time format to SRT time format."""
    h, m, s = ass_time.split(":")
    s, ms = s.split(".")
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int(ms)*10:03}"


def convert_ass_to_srt(ass_path, srt_path):
    try:
        with open(ass_path, 'r', encoding='utf-8') as ass_file:
            lines = ass_file.readlines()
        
        # Filter dialogue lines
        dialogue_lines = [line for line in lines if line.startswith("Dialogue:")]
        
        srt_lines = []
        for i, line in enumerate(dialogue_lines, start=1):
            parts = line.split(",", 9)  # Split ASS dialogue line into components
            if len(parts) < 10:
                continue  # Skip malformed lines
            
            start_time = convert_time(parts[1])
            end_time = convert_time(parts[2])
            text = re.sub(r'{.*?}', '', parts[9]).strip()  # Remove formatting tags
            
            srt_lines.append(f"{i}\n{start_time} --> {end_time}\n{text}\n")
        
        with open(srt_path, 'w', encoding='utf-8') as srt_file:
            srt_file.writelines(srt_lines)
        
        print(f"Successfully converted {ass_path} to {srt_path}")
        return True
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False




def hardcode_subtitles(video_path, subtitle_path, output_path):
    """
    Hardcodes subtitles into a video by first converting the .ass file to .srt
    and then using the .srt file to merge the subtitles into the video.
    """
    # Check if the input video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return False
    
    # Check if the subtitle file exists
    if not os.path.exists(subtitle_path):
        print(f"Error: Subtitle file '{subtitle_path}' not found.")
        return False

    # Generate the output SRT path (same as input subtitle path, but with .srt extension)
    srt_subtitle_path = subtitle_path.rsplit('.', 1)[0] + '.srt'
    
    # Step 1: Convert .ass to .srt
    if not convert_ass_to_srt(subtitle_path, srt_subtitle_path):
        print("Subtitle conversion failed. Aborting.")
        return False
    
    cmd = [
        'ffmpeg', 
        '-loglevel', 'debug',
        '-i', video_path,          # Input video file (for video stream)
        '-i', 'audio_jpn.m4a',     # Input audio file (for audio stream)
        '-vf', f"subtitles={srt_subtitle_path}",  # Hardcode subtitles filter
        '-map', '0:v:0',           # Map the video stream from the first input
        '-map', '1:a:0',           # Map the audio stream from the second input
        '-c:v', 'libx264',         # Video codec (H.264)
        '-c:a', 'aac',             # Audio codec (AAC, to ensure compatibility)
        output_path                # Output file with hardcoded subtitles and specified audio
    ]

    
    # Execute the command to hardcode subtitles
    try:
        subprocess.run(cmd, check=True)
        print(f"Subtitles have been successfully hardcoded into the video. Output saved as: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg execution: {e}")
        return False

# Object representing the video information
obj = {
    "title": "file.mkv\nOwner hidden\n8 May 2022\n357.8 MB",
    "href": "https://drive.google.com/file/d/1fDzOWm6YBpqRetZIWopAy962ADf5r6nv/view?usp=drive_link"
}


# Download the file
file_name = start_downloading(obj)
file_name = 'file.mkv'  # Assuming file was downloaded as 'file.mkv'

# Process the file if it exists
if file_name and os.path.exists(file_name):
    flag_result = get_meta_data(file_name)  # Get metadata
    
    if flag_result:
        subtitle_file = 'subtitle_1.ass'  # Input subtitle file
        output_file = 'output_file.mkv'  # Output video file

        try:
            # Call the function to hardcode subtitles
            success = hardcode_subtitles(file_name, subtitle_file, output_file)
            if success:
                print("Subtitle hardcoding completed.")
                videos_folder = split_video(output_file)

                if os.path.exists(videos_folder):
                    files_lst = os.listdir(videos_folder)
                    for file in files_lst:    
                        file = os.path.join(videos_folder,file)    
                        if os.path.exists(file):
                            mega = Mega()
                            keys = os.getenv('M_TOKEN')  # Get credentials from environment
                            if keys:
                                keys = keys.split("_")
                                try:
                                    m = mega.login(keys[0], keys[1])
                                    m.upload(file)
                                    print("File uploaded successfully to Mega.")
                                except Exception as e:
                                    print(f"Error uploading file to Mega: {e}")
                            else:
                                print("Mega credentials not found in environment variables.")
            
        except Exception as e:
            print(f"Error during subtitle hardcoding process: {e}")
else:
    print(f"{file_name} not found or failed to download.")
