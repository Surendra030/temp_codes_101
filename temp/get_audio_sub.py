import subprocess
import re
import os

# Specify the video file
def get_meta_data(video_file):
        
    # Output folder for extracted files
    output_folder = os.getcwd()
    # Path to the locally stored ffmpeg binary (relative path to your repository)
    ffmpeg_path = 'ffmpeg'  # Adjust this path based on where ffmpeg is stored in your repo
    # FFmpeg command to list all streams
    command_list_streams = [ffmpeg_path, "-i", video_file]
    codec_lst = []
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

        audio_codec = set()
        # Extract audio streams
        for i, (stream, codec) in enumerate(audio_streams, start=0):
            lang = languages.get(audio_streams_data[i][0],"Unknown")
            audio_file = f"audio_{lang}.{extension}"
            extension = codec if (codec != "aac") or (codec != 'srt') else "m4a"  # Use .m4a for AAC (more common)
            output_audio = os.path.join(output_folder, audio_file)
            extract_audio_command = [
                "ffmpeg", "-i", video_file, "-map", f"{stream}", "-c", "copy", output_audio
            ]
            audio_codec.add(audio_file)
            
            subprocess.run(extract_audio_command, check=True)
        
        subtitle_codecs = set()
            # Extract subtitle streams
        for i, (stream, codec) in enumerate(subtitle_streams, start=0):
                # Determine subtitle extension based on codec
            if codec == 'srt':
                extension = "srt"
            elif codec == 'ass':
                extension = "ass"
            elif codec == 'subrip':
                extension = "sub"
            else:
                extension = "ass"  # Default to .ass if codec is not recognized

            output_subtitle = os.path.join(output_folder, f"subtitle_{i}.{extension}")
                
                # Command to extract subtitle stream using ffmpeg
            extract_subtitle_command = [
                    "ffmpeg", "-i", video_file, "-map", f"{stream}", "-c", "copy", output_subtitle
            ]
                
            subprocess.run(extract_subtitle_command, check=True)
            print(f"Extracted Subtitle Stream {i} to {output_subtitle}")
            subtitle_codecs.add(codec)

        codec_lst.append({
            'subtitle_codecs':subtitle_codecs
        })


        return codec_lst if len(codec_lst>0) else None
    except Exception as e:
        print(f"Error occurred: {e}")
