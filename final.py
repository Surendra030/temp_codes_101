import traceback

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
    sanitized_title = re.sub(r'[\[\(].*?[\]\)]', '', title)
    sanitized_title = sanitized_title.strip()

    return sanitized_title

import re

def sanitize_folder(title: str) -> str:
    # Remove content inside [] and () along with the brackets themselves
    sanitized_title = re.sub(r'[\[\(].*?[\]\)]', '', title)
    # Remove extra spaces from the start and end
    sanitized_title = sanitized_title.strip()
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





def hardcode_subtitles(video_path, subtitle_path, audio_path, output_path):
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
    
    if '.ass' in str(subtitle_path):
        # Generate the output SRT path (same as input subtitle path, but with .srt extension)
        srt_subtitle_path = subtitle_path.rsplit('.', 1)[0] + '.srt'
        
        # Step 1: Convert .ass to .srt
        print(f"Converting subtitle file {subtitle_path} to {srt_subtitle_path}...")
        if not convert_ass_to_srt(subtitle_path, srt_subtitle_path):
            print("Subtitle conversion failed. Aborting.")
            return False
        else:
            print(f"Subtitle conversion successful: {srt_subtitle_path}")
    
    # Check the paths of all inputs before calling ffmpeg
    print(f"Video path: {video_path}")
    print(f"Audio path: {audio_path}")
    print(f"Subtitle path: {srt_subtitle_path}")
    print(f"Output path: {output_path}")
    
    cmd = [
        'ffmpeg', 
        '-loglevel', 'debug',
        '-i', video_path,          # Input video file (for video stream)
        '-i', audio_path,          # Input audio file (for audio stream)
        '-vf', f"subtitles={srt_subtitle_path}",  # Hardcode subtitles filter
        '-map', '0:v:0',           # Map the video stream from the first input
        '-map', '1:a:0',           # Map the audio stream from the second input
        '-c:v', 'libx264',         # Video codec (H.264)
        '-c:a', 'aac',             # Audio codec (AAC, to ensure compatibility)
        output_path                # Output file with hardcoded subtitles and specified audio
    ]
    
    print("Executing ffmpeg command:")
    print(' '.join(cmd))  # Log the full ffmpeg command being executed
    
    # Execute the command to hardcode subtitles
    try:
        subprocess.run(cmd, check=True)
        print(f"Subtitles have been successfully hardcoded into the video. Output saved as: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg execution: {e}")
        print(video_path, subtitle_path, audio_path, output_path)

        return False







def main_fun(obj_data_lst):
    try:
        # Initial check for data length
        if len(obj_data_lst['data']) >= 2:
            folder_name = obj_data_lst['data'][0]['title']
            folder_name = sanitize_folder(folder_name)
            print(folder_name)
        
        for index, obj in enumerate(obj_data_lst['data'][1:2]):
            try:
                print(f"Processing index {index}: {obj.get('title', 'Unknown Title')}")
                
                title_splits = obj['title'].split("\n")
                title = title_splits[0]
                file_name = sanitize_title(title)  # Sanitize title for filename
 
                # Download the file
                file_name_downloaded = start_downloading(obj)
                

                # Check if file exists
                if os.path.exists(file_name):

                    print(f"File exists: {file_name}. Retrieving metadata...")
                    audio_sub_codes_lst = get_meta_data(file_name)
                    audio_sub_codes_lst = audio_sub_codes_lst[0]
                    files = os.listdir()

                    if audio_sub_codes_lst:
                        audio_file_names = audio_sub_codes_lst['audio_codecs']
                        sub_codes = audio_sub_codes_lst['subtitle_codecs']


                        if 0< len(sub_codes) <=1 :
                            files_count = 0
                            print("none : ",sub_codes)
                            for file in files:
                                
                                if str(sub_codes[0]) in file:
                                    files_count +=1

                            subtitle_file = f"subtitle_{files_count-1}.{sub_codes[0]}"
                            output_file = f"{file_name.split(".")[0]}.mp4"

                            try:
                                audio_file_len = len(audio_file_names)
                                if audio_file_len > 0:

                                    if audio_file_len >= 2:
                                        success = hardcode_subtitles(file_name, subtitle_file, audio_file_names[0], output_file)
                                    else:
                                        success = hardcode_subtitles(file_name, subtitle_file, audio_file_names[0], output_file)

                                    if success:

                                        print("Subtitle hardcoding completed successfully.")
                                        videos_folder = split_video(output_file)
                                        print(f"Videos split into folder: {videos_folder}")
                                        
                                        # Upload to Mega
                                        mega = Mega()
                                        keys = os.getenv('M_TOKEN')
                                        if keys:
                                            keys = keys.split("_")
                                            keys[0] = keys[0].replace('6@', '8@')
                                            m = mega.login(keys[0], keys[1])

                                            file = m.create_folder(folder_name)
                                            folder_handle = file[folder_name]
                                            
                                            if os.path.exists(videos_folder):
                                                files_lst = os.listdir(videos_folder)
                                                for file in files_lst:
                                                    file_path = os.path.join(videos_folder, file)
                                                    if os.path.exists(file_path):
                                                        try:
                                                            m.upload(file_path, folder_handle)
                                                            print(f"Uploaded: {file_path} to Mega.")
                                                        except Exception as e:
                                                            print(f"Error uploading file '{file_path}' to Mega: {e}")
                                                            traceback.print_exc()

                                                os.remove(file_name)

                                        else:
                                            print("Mega credentials not found in environment variables.")
                                    else:
                                        print("Subtitle hardcoding failed.")
                            except Exception as e:
                                print(f"Error during subtitle hardcoding process: {e}")
                                traceback.print_exc()
                        else:
                            print(f"No valid subtitles found for {file_name}.")
                    else:
                        print(f"No metadata returned for {file_name}.")
                else:
                    print(f"File not found: {file_name}. Skipping...")
                
            except Exception as e:
                print(f"Error at index {index}: {e}")
                traceback.print_exc()
                continue

        print("Processing of all files completed.")
     
    except Exception as e:
        print(f"Critical error in main function: {e}")
        traceback.print_exc()
