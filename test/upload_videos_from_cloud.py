from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from encrypt_decrypt.decrypt import decrypt_json
from cloud_related import download_video,get_video_links
from utils.process_video import process_video_file
from googleapiclient.errors import HttpError

import os


def upload_video_to_playlist(youtube, video_file, title, description, playlist_id, category_id="22", privacy_status="public"):
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
        add_video_to_playlist(youtube, video_id, playlist_id)
    
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        # Additional logging can be added if necessary
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Additional logging can be added if necessary


def add_video_to_playlist(youtube, video_id, playlist_id):
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
        print(f"Video added to playlist: {playlist_id}!")
    
    except HttpError as e:
        print(f"An HTTP error occurred while adding to the playlist: {e}")
        # Additional logging can be added if necessary
    except Exception as e:
        print(f"An unexpected error occurred while adding to the playlist: {e}")
        # Additional logging can be added if necessary


passphrase = os.getenv("PASSWORD")
parent_handle = 'p0pR3D4C'

print(os.listdir())
decrypted_data = decrypt_json("encrypted_data.json", passphrase)
videos_links_data = get_video_links(parent_handle)

# Load credentials from the token.json file (assuming you've already authenticated)
credentials = Credentials.from_authorized_user_info(decrypted_data, ['https://www.googleapis.com/auth/youtube.upload'])

# Create the YouTube API client
youtube = build('youtube', 'v3', credentials=credentials)




for index,video_obj in enumerate(videos_links_data):
    
    link = video_obj['link']
    file_name = video_obj['file_name']

    video_downloded_path = download_video(link)
    
    if video_downloded_path:
        playlist_id = "PLMfzrR_Qa8ifWH43CsVL_jqEfzkLVJFcO"  # Replace with your playlist ID
        # Dynamically generate description using the file_name
        
        temp_name = file_name.split(".")[0]
        description = f"{temp_name} is an exciting and captivating video. In this video, we explore the details of {temp_name} and provide a comprehensive look into its content."

        video_sub_parts = process_video_file(video_downloded_path,temp_name)
        
        for video_obj in video_sub_parts:
            video_path = video_obj['videopath']
            video_name = video_obj['video_name']
            
            try:
                if os.path.exists(video_path):
                    upload_video_to_playlist(youtube, video_path, video_name, description, playlist_id)
            except Exception as e:
                print("Error failed to upload video : ",e)