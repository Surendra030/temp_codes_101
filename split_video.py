import json
import shutil
import subprocess
import math
import os

def get_folder_size(folder_path):
    """Calculate the total size of a folder (including subfolders and files)."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def get_video_duration(file_path):
    """Get the duration of the video in seconds using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        return 0

def split_video(file_path, segment_duration=5 * 60):
    """Split the video into parts of the specified duration."""
    try:
        total_duration = get_video_duration(file_path)
        if total_duration == 0:
            print(f"Skipping {file_path}: Unable to determine duration.")
            return None
        
        total_segments = math.ceil(total_duration / segment_duration)
        file_name, file_ext = os.path.splitext(file_path)
        file_name = f"{file_name}_do_not_remove_final"
        videos_folder = f'{file_name}_videos'
        os.makedirs(videos_folder, exist_ok=True)

        for i in range(total_segments):
            start_time = i * segment_duration
            output_file = os.path.join(videos_folder, f"{file_name}_part{i + 1}{file_ext}")
            command = [
                "ffmpeg", "-i", file_path, "-ss", str(start_time), "-t", str(segment_duration),
                "-c", "copy", output_file
            ]
            print(f"Processing segment {i + 1}/{total_segments}: {output_file}")
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"Video splitting completed for {file_path}!")
        os.remove(file_path)
        return videos_folder
    except Exception as e:
        print(f"Error splitting video {file_path}: {e}")
        return None



def split_video_main():
    # Main Script
    files = os.listdir()
    files_lst = [file for file in files if 'hardcoded.' in file and file.endswith(('.mp4', '.avi', '.mkv'))]  # Filter for video files
    hardcoded_files = []
    folder_name_lst = []
    
    if len(files_lst) > 0:
        for file in files_lst:
            videos_folder = split_video(file)  # Call your split_video function
            if videos_folder:

                folder_size = get_folder_size(videos_folder)  # Call your get_folder_size function
                if folder_size > 0:
                    hardcoded_files.append({
                        "folder": videos_folder, 
                        "size_MB": round(folder_size / (1024 * 1024), 2)  # Convert to MB with 2 decimal places
                    })
                    folder_name_lst.append(videos_folder)  # Store folder name in the list
                    os.remove(file)
        # Save the list of processed  to JSON

    else:
        print("No files with 'hardcoded' in their name found.")

    return folder_name_lst if len(folder_name_lst)>0 else None

