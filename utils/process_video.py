from moviepy.editor import VideoFileClip
import os

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
    temp_folder = "temp/videos"
    os.makedirs(temp_folder, exist_ok=True)
    
    video_parts = []
    
    # Split the video into parts
    for i in range(num_parts):
        start_time = i * part_duration
        end_time = min((i + 1) * part_duration, video_duration)
        
        # Create the video part using the subclip method
        video_part = video.subclip(start_time, end_time)
        
        # Name the video part (e.g., video_part_1, video_part_2, etc.)
        temp_name = f"{filename}_video_part_{i + 1}.mp4"
        temp_path = os.path.join(temp_folder, temp_name)
        
        # Write the part to the temp folder
        video_part.write_videofile(temp_path, codec="libx264", audio_codec="aac")
        
        # Add the part to the video_parts list
        video_parts.append({
            'videopath': temp_path,
            'video_name': temp_name
        })

    # Close the video file
    video.close()
    
    return video_parts
