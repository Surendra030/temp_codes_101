import os
from pydub import AudioSegment

def add_m_l(file_path):
        
    try:
            
        # Load the audio files
        original = AudioSegment.from_mp3(file_path)
        middle = AudioSegment.from_mp3("middle.mp3")
        last = AudioSegment.from_mp3("last.mp3")

        # Get the duration of the original file in seconds
        original_duration = len(original) // 1000  # Convert milliseconds to seconds

        # Calculate the midpoint in seconds
        midpoint_seconds = original_duration // 2

        # Adjust the midpoint to the nearest value divisible by 5
        if midpoint_seconds % 5 != 0:
            midpoint_seconds += (5 - (midpoint_seconds % 5))

        # Split the original audio at the adjusted midpoint (in seconds)
        first_half = original[:midpoint_seconds * 1000]  # Convert seconds to milliseconds
        second_half = original[midpoint_seconds * 1000:]  # Convert seconds to milliseconds

        # Trim and modify the second half
        trimmed_second_half = second_half[91 * 1000: -90 * 1000]  # Trim in seconds, converted to milliseconds
        second_half_modified = middle + trimmed_second_half + last

        # Combine all parts
        final_audio = first_half + second_half_modified

        temp_path = 'temp_audio.mp3'
        # Export the final audio
        final_audio.export(temp_path, format="mp3")
        return temp_path if os.path.exists(temp_path) else None
    
    except Exception as e:
        print("Error failed :",e)
