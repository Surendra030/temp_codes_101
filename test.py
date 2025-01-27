from pydub.utils import mediainfo
from pydub import AudioSegment
from add_middle_last import add_m_l
import os
import subprocess
import json
from get_mega_instance import fetch_m

def upload_files(video_path):
    m = fetch_m()
    fd = 'video_files'
    file = m.create_folder(fd)
    fh = file[fd]
    try:
        link = m.upload(video_path,fh)
        return link if link else None
    except Exception as e:
        print("Error :",e)

def add_audio_to_video(audio_file_path, video_file_path):
    # Output video file path
    temp_video_path = "temp_video.mp4"
    
    # FFmpeg command to overlay audio on video
    command = [
        'ffmpeg',
        '-i', video_file_path,  # Input video
        '-i', audio_file_path,  # Input audio
        '-c:v', 'libx264',       # Video codec
        '-c:a', 'aac',           # Audio codec
        '-strict', 'experimental', # Allow experimental codecs
        '-shortest',             # Make the output video as long as the shortest input (video/audio)
        temp_video_path         # Output video path
    ]
    
    print(f"Running FFmpeg command to add audio to video: {command}")
    
    # Run the FFmpeg command
    subprocess.run(command, check=True)
    
    print(f"Audio successfully added to video. Saved as: {temp_video_path}")
    
    # Return the saved video file path
    return temp_video_path


def trim_audio(input_file, output_file, duration_in_seconds):
    print(f"Trimming audio from: {input_file} to {output_file} for {duration_in_seconds} seconds.")
    
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Calculate the trimming range
    trim_duration = duration_in_seconds * 1000  # Convert seconds to milliseconds
    
    # Trim the audio
    trimmed_audio = audio[:trim_duration]
    
    # Save the trimmed audio to the output file
    trimmed_audio.export(output_file, format="mp3")
    
    if os.path.exists(output_file):
        print(f"Trimmed audio saved as: {output_file}")
        return output_file
    else:
        print(f"Failed to save trimmed audio.")
        return None

def get_video_duration(file_path):
    print(f"Getting duration of video: {file_path}")
    
    # Get video information using pydub
    video_info = mediainfo(file_path)

    # Extract the duration in seconds
    duration_in_seconds = int(float(video_info['duration']))
    
    if duration_in_seconds:
        print(f"Video duration is {duration_in_seconds} seconds.")
    else:
        print(f"Failed to retrieve video duration.")
        
    return duration_in_seconds if duration_in_seconds else None


file_name_data  = 'temp.json'

with open(file_name_data,'r')as f:
    data_obj = json.load(f)
final_data = []

m = fetch_m()

#625
start = 0
end = start + 1
data_obj = data_obj[start:end]

try:
        
    for obj in data_obj:
        try:
            fo_path = None

            video_path = obj['fileName']
            link = obj['link']
            try:
                m.download_url(link)
            except Exception as e:
                print("Error failed to download :",e)
                
            duration_in_seconds = get_video_duration(video_path)

            # File paths and duration
            input_audio_path = r"t.mp3"
            output_audio_path = r"trimmed_audio.mp3"

            if duration_in_seconds:
                output_file = trim_audio(input_audio_path, output_audio_path, duration_in_seconds)
                if output_file and os.path.exists(output_file):
                    print(f"Adding middle and last parts to the audio.")
                    add_m_l_file_path = add_m_l(output_file)

                    if add_m_l_file_path and os.path.exists(add_m_l_file_path):
                        print(f"Adding audio to video.")
                        final_video_path = add_audio_to_video(add_m_l_file_path, video_path)
                        if final_video_path and os.path.exists(final_video_path):
                            print(f"Final video created: {final_video_path}")
                            
                            # Clean up temporary files
                            os.remove(add_m_l_file_path)
                            os.remove(output_file)
                            print(f"Temporary files removed")
                            os.remove(video_path)
                            os.rename(final_video_path,video_path)
                            flag = upload_files(video_path)
                            if flag:
                                final_data.append({
                                    "link":flag,
                                    "fn":video_path
                                })
                                os.remove(video_path)
                            print("Renaming the file completed..")
                        else:
                            print(f"Failed to create final video.")
                    else:
                        print(f"Failed to add middle and last parts to audio.")
                else:
                    print(f"Failed to trim audio or audio file not found.")
            else:
                print(f"Invalid video duration or video file not found.")
        finally:
            files = os.listdir()
            for f in files:
                if '.mp4' in f:
                    os.remove(f)
            
finally:
    fs = "video_links_modified.json"
    with open(fs,'w'):
        json.dump(final_data,f,indent=4)
    m = fetch_m()
    m.upload(fs)