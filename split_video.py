import subprocess
import math
import os

def get_video_duration(file_path):
    """Get the duration of the video in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
         check=True, stdout=subprocess.DEVNULL
    )
    return float(result.stdout.strip())

def split_video(file_path, segment_duration=5 * 60):
    """Split the video into parts of the specified duration."""
    total_duration = get_video_duration(file_path)
    total_segments = math.ceil(total_duration / segment_duration)
    file_name, file_ext = os.path.splitext(file_path)
    
    for i in range(total_segments):
        try:
            start_time = i * segment_duration
            output_file = f"{file_name}_part{i + 1}{file_ext}"
            videos_folder = 'videos'
            
            os.makedirs(videos_folder,exist_ok=True)
            output_file = os.path.join(videos_folder,output_file)
            
            command = [
                "ffmpeg", "-i", file_path, "-ss", str(start_time), "-t", str(segment_duration),
                "-c", "copy", output_file
            ]
            print(f"Processing segment {i + 1}/{total_segments}: {output_file}")
            subprocess.run(command)
        except Exception as e:
            print("Error : ",e)
    print("Video splitting completed!")
    return videos_folder

