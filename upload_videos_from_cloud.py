from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from encrypt_decrypt.decrypt import decrypt_json
from cloud_related.download_video import download_file_from_link
from utils.process_video import process_video_file
from cloud_related.get_video_links import get_files_with_links
from googleapiclient.errors import HttpError
import os


def upload_video_to_playlist(youtube, video_file, title, description, playlist_id, category_id="22", privacy_status="public"):
    print(f"Starting upload for video: {title}")
    try:
        # Upload the video to YouTube
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
            },
        }

        # Upload the media
        print(f"Uploading video file: {video_file}")
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )
        response = request.execute()
        video_id = response["id"]
        print(f"Video uploaded successfully! Video ID: {video_id}")

        # Add the uploaded video to the specified playlist
        print(f"Adding video to playlist with ID: {playlist_id}")
        add_video_to_playlist(youtube, video_id, playlist_id)

    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def add_video_to_playlist(youtube, video_id, playlist_id):
    print(f"Adding video {video_id} to playlist {playlist_id}")
    try:
        # Add the uploaded video to the playlist
        playlist_item = {
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                },
            }
        }
        request = youtube.playlistItems().insert(
            part="snippet",
            body=playlist_item
        )
        response = request.execute()
        print(f"Video successfully added to playlist: {playlist_id}")

    except HttpError as e:
        print(f"An HTTP error occurred while adding to the playlist: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while adding to the playlist: {e}")


# Start script
print("Decrypting credentials and fetching video links")
passphrase = "myApp101!"
parent_handle = 'pkxg1JyR'
decrypted_data = decrypt_json("encrypted_data.json", passphrase)

videos_links_data = get_files_with_links(parent_handle)

print("Creating YouTube API client")
# Load credentials from the token.json file (assuming you've already authenticated)
credentials = Credentials.from_authorized_user_info(decrypted_data, ['https://www.googleapis.com/auth/youtube.upload',
                                                                    'https://www.googleapis.com/auth/youtube.force-ssl',
                                                                    'https://www.googleapis.com/auth/youtube'])
youtube = build('youtube', 'v3', credentials=credentials)

# Process and upload videos
print(f"Processing {len(videos_links_data)} videos")
for index, video_obj in enumerate(videos_links_data):
    link = video_obj['link']
    file_name = video_obj['file_name']
    print(f"Downloading video {index + 1}/{len(videos_links_data)}: {file_name}")

    video_downloded_path = download_file_from_link(link)
    if os.path.exists(file_name):
        print(f"Downloaded video to: {file_name}")
        playlist_id = "PLMfzrR_Qa8ifwfcXkauBYJDFD7hI9IA-g"
        
        temp_name = file_name.split(".")[0]
        description = f"{temp_name} is an exciting and captivating video. In this video, we explore the details of {temp_name} and provide a comprehensive look into its content."

        print(f"Processing video for subparts: {file_name}")
        video_sub_parts = process_video_file(file_name, temp_name)

        for sub_index, video_obj in enumerate(video_sub_parts):
            video_path = video_obj['videopath']
            video_name = video_obj['video_name']
            print(f"Uploading sub-video {sub_index + 1}/{len(video_sub_parts)}: {video_name}")

            try:
                if os.path.exists(video_path):
                    print(f"Found video file: {video_path}")
                    upload_video_to_playlist(youtube, video_path, video_name, description, playlist_id)
                else:
                    print(f"Video file not found: {video_path}")
            except Exception as e:
                print(f"Error failed to upload video {video_name}: {e}")
    else:
        print(f"Failed to download video: {file_name}")
