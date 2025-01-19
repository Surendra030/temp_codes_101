import subprocess
import re
import os
import traceback

def sanitize_folder(title: str) -> str:
    """
    Sanitize the file name by removing content inside [] and (), along with the brackets.
    """
    sanitized_title = re.sub(r'[\[\(].*?[\]\)]', '', title)
    sanitized_title = sanitized_title.strip()  # Remove extra spaces
    return sanitized_title


def get_meta_data(video_file, index):
    """
    Extract audio and subtitle streams from a video file using FFmpeg.
    """
    ffmpeg_path = "ffmpeg"  # Ensure FFmpeg is installed and accessible via PATH
    command_list_streams = [ffmpeg_path, "-i", video_file]

    try:
        # Capture stderr where FFmpeg outputs stream details
        result = subprocess.run(command_list_streams, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        output = result.stderr

        # Regex patterns for audio and subtitle streams
        audio_pattern = r"Stream #(\d+:\d+).*: Audio: (\w+)"
        subtitle_pattern = r"Stream #(\d+:\d+).*: Subtitle: (\w+)"
        language_pattern = r"Stream #(\d+:\d+).*?\((\w+)\)"

        # Extract matches
        audio_streams = re.findall(audio_pattern, output)
        subtitle_streams = re.findall(subtitle_pattern, output)
        languages = dict(re.findall(language_pattern, output))
        print(audio_streams, subtitle_streams, languages)

        # Process audio streams
        for i, (stream, codec) in enumerate(audio_streams, start=0):
            lang = languages.get(stream, "Unknown")
            extension = "m4a" if codec == "aac" else codec  # Default to codec name if unknown
            audio_file = f"index_{index}_audio_{lang}_{i}.{extension}"
            output_audio = audio_file

            try:
                # Command to extract audio
                extract_audio_command = [
                    ffmpeg_path, "-i", video_file, "-map", f"{stream}", "-c", "copy", output_audio, "-y"
                ]
                subprocess.run(extract_audio_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Extracted Audio Stream {i} ({lang}) to {output_audio}")
            except Exception as e:
                print(f"Error extracting Audio Stream {i} ({lang}): {e}")
                traceback.print_exc()

        # Process subtitle streams
        for i, (stream, codec) in enumerate(subtitle_streams, start=0):
            # Handle unsupported codecs
            if codec == "dvd_subtitle":
                print(f"Skipping unsupported subtitle codec: {codec} (Stream {stream})")
                continue

            extension = "srt" if codec == "subrip" else codec  # Default to codec name if unknown
            subtitle_file = f"index_{index}_subtitle_{i}.{extension}"
            output_subtitle = subtitle_file

            try:
                # Command to extract subtitles
                extract_subtitle_command = [
                    ffmpeg_path, "-i", video_file, "-map", f"{stream}", "-c", "copy", output_subtitle, "-y"
                ]
                subprocess.run(extract_subtitle_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Extracted Subtitle Stream {i} to {output_subtitle}")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while processing subtitle stream {i}: {e}")
                print(f"Command: {' '.join(extract_subtitle_command)}")
            except Exception as ex:
                print(f"Unexpected error while processing subtitle stream {i}: {ex}")
                traceback.print_exc()

    except Exception as e:
        print(f"Error occurred while processing {video_file}: {e}")
        traceback.print_exc()


def meta_data_main():
    all_files = os.listdir()
    video_files = [file for file in all_files if file.endswith(('.mkv', '.mp4'))]

    for index, video in enumerate(video_files):
        try:
            sanitized_name = sanitize_folder(video)
            if sanitized_name != video:
                os.rename(video, sanitized_name)  # Rename if necessary
                video = sanitized_name

            print(f"Processing {video}...")
            get_meta_data(video, index)
        except Exception as e:
            print(f"Error occurred while processing {video}: {e}")
            traceback.print_exc()


