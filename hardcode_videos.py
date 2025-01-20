import os
import subprocess
from mega import Mega
import re
import traceback




def convert_time(ass_time):
    """Convert ASS time format to SRT time format."""
    h, m, s = ass_time.split(":")
    s, ms = s.split(".")
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int(ms)*10:03}"



def convert_ass_to_srt(ass_path, srt_path):
    if os.path.exists(srt_path):
        os.remove(srt_path)
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
    
    if '.ass' in str(subtitle_path) or '.srt' in str(subtitle_path) :
        # Generate the output SRT path (same as input subtitle path, but with .srt extension)
        
        srt_subtitle_path = str(subtitle_path).split('.')[0] + '.srt'
        
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
        output_path ,
        '-y'              # Output file with hardcoded subtitles and specified audio
    ]
    
    print("Executing ffmpeg command:")
    print(' '.join(cmd))  # Log the full ffmpeg command being executed
    
    # Execute the command to hardcode subtitles
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"Subtitles have been successfully hardcoded into the video. Output saved as: {output_path}")
        os.remove(srt_subtitle_path)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg execution: {e}")
        print(video_path, subtitle_path, audio_path, output_path)

        return False


def count_words_in_file(file_path):
    """
    Counts the number of words in a given file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return len(content.split())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def hardcode_all_videos():
        

    all_files = os.listdir()
    video_file = []

    for index, file in enumerate(all_files):


        if '.mkv' in file or '.mp4' in file:
            video_file.append(file)
            

    for index,video in enumerate(video_file):
        audio_files = []
        sub_files = []
        for file in all_files:
        # Collect audio and subtitle files for the current index
            if f'index_{index}_audio' in file:
                audio_files.append(file)

            if f'.ass' in file or '.srt' in file:
                sub_files.append(file)
                
        # Get the last audio file if available
        a_file = audio_files[-1] if len(audio_files) >= 1 else audio_files[0]

        # Find the subtitle file with the largest word count
        if sub_files:
            subtitle_word_counts = {sub_file: count_words_in_file(sub_file) for sub_file in sub_files}
            # Sort by word count and get the file with the highest count
            s_file = max(subtitle_word_counts, key=subtitle_word_counts.get)
        else:
            print("Using else case for subtitles files..\n",sub_files)
            s_file = sub_files[0]

        if s_file and a_file:

            output_file = f'{str(video).split('.')[0]}_hardcoded.mp4'
            hardcode_flag = hardcode_subtitles(video,s_file,a_file,output_file)
            if os.path.exists(output_file):
                    
                try:
                    os.remove(video)
                    for sfile in sub_files:
                        os.remove(sfile)
                    for afile in audio_files:
                        os.remove(afile)

                except Exception as e:
                    print("Error ",e)   
        else:
            print("not working..")     