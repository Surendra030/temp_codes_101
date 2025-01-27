from pydub import AudioSegment

def add_silence(input_file, duration_in_seconds, output_file):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Generate silence of the specified duration
    silence = AudioSegment.silent(duration=duration_in_seconds * 1000)  # Duration in milliseconds
    
    # Append silence to the audio
    modified_audio = audio + silence
    
    # Save the modified audio to the output file
    modified_audio.export(output_file, format="mp3")
    print(f"Modified audio saved as: {output_file}")


# File paths and duration
input_audio_path = "middle.mp3"  # Input audio file
silence_duration = 10        # Silence duration in seconds
output_audio_path = input_audio_path.replace(".mp3", "_modified.mp3")

add_silence(input_audio_path, silence_duration, output_audio_path)

#
