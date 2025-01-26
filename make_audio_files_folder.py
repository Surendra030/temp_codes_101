from gtts import gTTS
from pydub import AudioSegment
import os
from pydub.utils import mediainfo


def get_video_duration(video_file):

    # Get media information
    info = mediainfo(video_file)
 
    # Extract and print the duration (in seconds)
    duration_in_seconds = int(float(info['duration']))  # Duration is provided in milliseconds
    return duration_in_seconds if duration_in_seconds else None




# Function to generate and save TTS audio for a given text
def generate_audio(text, filename):
    tts = gTTS(text, lang='en')
    tts.save(filename)

def main_file(file,audio_files):
    
    try:
            
        total_duration = get_video_duration(file)
        # Number of parts (60 parts)
        num_parts = total_duration//5
        # Duration of each part in seconds

        os.makedirs(audio_files,exist_ok=True)
        # Generate and save audio for each page number
        for i in range(1, num_parts + 1):
            page_text = f"Page {i}"
            filename = f"./audio_files/part_{i}.mp3"
            
            generate_audio(page_text, filename)
        return True
    except Exception as e:
        print("Error failed to make folder : ",e)
            
