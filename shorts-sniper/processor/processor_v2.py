import hashlib
from typing import Dict, Any
from pytube import YouTube, Playlist
from youtube_transcript_api import YouTubeTranscriptApi
from mongodb.mongodb import MongoDBClient

def generate_unique_id(my_dict):
    # Concatenate relevant attributes
    concatenated_string = f"{my_dict['text']}_{my_dict['start']}_{my_dict['duration']}_{my_dict['videoId']}"

    # Hash the concatenated string
    hashed_value = hashlib.md5(concatenated_string.encode()).hexdigest()

    return hashed_value

def get_playlist_video_urls(playlist_url):
    playlist = Playlist(playlist_url)

    video_urls = list(playlist.url_generator())
    return video_urls


import time

def process_videos_by_video_urls(video_urls: [str]) -> None:
    try:
        total_videos = len(video_urls)
        video_processed_count = 0
        start_time = time.time()

        for url in video_urls:
            process_single_video(url)
            video_processed_count += 1
            elapsed_time = time.time() - start_time
            average_time_per_video = elapsed_time / video_processed_count
            remaining_videos = total_videos - video_processed_count
            estimated_remaining_time = remaining_videos * average_time_per_video
            remaining_time_str = time.strftime("%H:%M", time.gmtime(estimated_remaining_time))
            
            print(f"Processed {video_processed_count}/{total_videos} videos | Estimated remaining time: {remaining_time_str}", end='\r', flush=True)

        print()  # Move to the next line after completion
    except Exception as e:
        print(f"Error on process_videos_by_channel_url: {str(e)}")



def process_single_video(video_url: str) -> None:
    try:
        video_data: Dict[str, Any] = extract_video_data_by_video_url(video_url)

        video_id: str = video_data["infos"]["videoId"]

        mongo_client_for_transcriptions: MongoDBClient = MongoDBClient(
            collection_name="videoData"
        )
        mongo_client_for_transcriptions.insert_document(
            document=video_data["infos"], document_id=video_id
        )

        mongo_client_for_video_data: MongoDBClient = MongoDBClient(
            collection_name="videoTranscriptionsV2"
        )
                
        transcripts: [dict] = video_data["transcript"]['transcript']
        
        # Loop over each transcript and insert it into the collection
        for transcript_entry in transcripts:
            id = generate_unique_id(transcript_entry)
            mongo_client_for_video_data.insert_document(
                document=transcript_entry, document_id=id
            )
    except Exception as e:
        print(f"Error processing video {video_url}: {str(e)}")


def extract_video_data_by_video_url(video_url: str) -> Dict[str, Dict[str, Any]]:
    try:
        youtube_video: YouTube = YouTube(video_url)

        video_id: str = youtube_video.video_id
        transcript: Dict[str, str] = YouTubeTranscriptApi.get_transcripts(
            [video_id], languages=["pt", "en"]
        )

        transcript_array = transcript[0][video_id]
        
        # Iterate over transcript items and add "videoId" key to each dictionary
        modified_transcript = [
            {**item, "videoId": video_id} for item in transcript_array
        ]

        return {
            "infos": {
                **youtube_video.vid_info["videoDetails"],
                "watchUrl": youtube_video.watch_url,
                "videoId": video_id,
            },
            "transcript": {
                "transcript": modified_transcript,
            },
        }
    except Exception as e:
        print(f"Error extracting data for video {video_url}: {str(e)}")
        