from download_video import start_downloading
from get_audio_sub import get_meta_data
from split_video import split_video

import os
import subprocess
from mega import Mega
import re

def sanitize_title(title):
    """
    Sanitize the title to create a valid filename by removing unwanted characters.
    """
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)
    return sanitized_title


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




def hardcode_subtitles(video_path, subtitle_path,audio_path, output_path):
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
    
    if '.ass' in  str(subtitle_path):
        # Generate the output SRT path (same as input subtitle path, but with .srt extension)
        srt_subtitle_path = subtitle_path.rsplit('.', 1)[0] + '.srt'
        
        # Step 1: Convert .ass to .srt
        if not convert_ass_to_srt(subtitle_path, srt_subtitle_path):
            print("Subtitle conversion failed. Aborting.")
            return False
        else: srt_subtitle_path = subtitle_path
    
    cmd = [
        'ffmpeg', 
        '-loglevel', 'debug',
        '-i', video_path,          # Input video file (for video stream)
        '-i', audio_path,     # Input audio file (for audio stream)
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



def main_fun(obj_data_lst):
    if len(obj_data_lst['data'])>=2:

        folder_name =obj_data_lst['data'][0]['title']
        folder_name = sanitize_title(folder_name)
        obj_data_lst = obj_data_lst[1:]
        
    for index,obj in enumerate(obj_data_lst['data']):
        
        try:
                
            title_splits = obj['title'].split("\n")

            title = title_splits[0]

            file_name = sanitize_title(title)# Download the file
            file_name = start_downloading(obj)

            # Process the file if it exists
            if file_name and os.path.exists(file_name):
                audio_sub_codes_lst = get_meta_data(file_name)  # Get metadata
                
                if audio_sub_codes_lst:
                    audio_file_names = audio_sub_codes_lst[0]
                    sub_codes = audio_sub_codes_lst[1]

                    if len(sub_codes)> 0:
                        if len(sub_codes) >=2:
                            subtitle_file = f'subtitle_1.{sub_codes[1]}'  # Input subtitle file
                        else:
                            subtitle_file = f'subtitle_1.{sub_codes[0]}'  # Input subtitle file
                        output_file = 'output_file.mkv'  # Output video file

                        try:
                            audio_file_len = len( audio_file_names)
                            if audio_file_len>0:
                            # Call the function to hardcode subtitles
                                if audio_file_len>=2:
                                    
                                    success = hardcode_subtitles(file_name, subtitle_file,audio_file_names[1], output_file)
                                if audio_file_len<2:
                                    success = hardcode_subtitles(file_name, subtitle_file,audio_file_names[0], output_file)

                                
                                if success:
                                    print("Subtitle hardcoding completed.")
                                    videos_folder = split_video(output_file)
                                    mega = Mega()
                                    keys = os.getenv('M_TOKEN')

                                    keys = keys.split("_")
                                    keys[0] = keys[0].replace('6@','8@')
                                    m = mega.login(keys[0], keys[1])

                                    file = m.create_folder(folder_name)
                                    folder_handle  = file[folder_name]
                                    if os.path.exists(videos_folder):
                                        files_lst = os.listdir(videos_folder)
                                        for file in files_lst:    
                                            file = os.path.join(videos_folder,file)    
                                            if os.path.exists(file):
                                                if keys:
                                                    
                                                    try:
                                                        m.upload(file,folder_handle)

                                                        print("File uploaded successfully to Mega.")
                                                    except Exception as e:
                                                        print(f"Error uploading file to Mega: {e}")
                                                else:
                                                    print("Mega credentials not found in environment variables.")
                                
                        except Exception as e:
                            print(f"Error during subtitle hardcoding process: {e}")
                    else:
                        print(f"{file_name} not found or failed to download.")
            print("Processing all file completed..")
        except Exception as e:
            print(f"Error in {index}: ",e)