import subprocess
import re
import os

# Specify the video file
def get_meta_data(video_file):
        
    # Output folder for extracted files
    output_folder = "extracted_streams"
    os.makedirs(output_folder, exist_ok=True)

    # FFmpeg command to list all streams
    command_list_streams = ["ffmpeg", "-i", video_file]

    try:
        # Run the command and capture the stderr output
        result = subprocess.run(command_list_streams, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        output = result.stderr

        # Extract audio and subtitle streams
        audio_pattern = r"Stream #(\d+:\d+).*: Audio: (\w+)"
        audio_pattern_lang = r"Stream #(\d+:\d+).*: Audio: (.+)"

        subtitle_pattern = r"Stream #(\d+:\d+).*: Subtitle: (\w+)"
        language_pattern = r"Stream #(\d+:\d+).*?\((\w+)\)"

        audio_streams = re.findall(audio_pattern, output)
        subtitle_streams = re.findall(subtitle_pattern, output)

        audio_pattern_data = r"Stream #(\d+:\d+).*: Audio: (\w+)"
        audio_streams_data = re.findall(audio_pattern_data, output)

        subtitle_pattern_data = r"Stream #(\d+:\d+).*: Subtitle: (.+)"
        subtitle_streams_data = re.findall(subtitle_pattern, output)



        languages = dict(re.findall(language_pattern, output))

        # Extract audio streams
        for i, (stream, codec) in enumerate(audio_streams, start=0):
            lang = languages.get(audio_streams_data[i][0],"Unknown")

            extension = codec if codec != "aac" else "m4a"  # Use .m4a for AAC (more common)
            output_audio = os.path.join(output_folder, f"audio_{lang}.{extension}")
            extract_audio_command = [
                "ffmpeg", "-i", video_file, "-map", f"{stream}", "-c", "copy", output_audio
            ]
            subprocess.run(extract_audio_command, check=True)


        # Extract subtitle streams
        for i, (stream, codec) in enumerate(subtitle_streams, start=0):
            
            extension = subtitle_streams_data[i][1]
            output_subtitle = os.path.join(output_folder, f"subtitle_{i}.ass")
            extract_subtitle_command = [
                "ffmpeg", "-i", video_file, "-map", f"{stream}", "-c", "copy", output_subtitle
            ]
            subprocess.run(extract_subtitle_command, check=True)
            print(f"Extracted Subtitle Stream {i} to {output_subtitle}")
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
