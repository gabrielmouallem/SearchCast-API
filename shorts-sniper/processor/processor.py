from typing import List, Dict, Any
from pytube import YouTube, Playlist
from youtube_transcript_api import YouTubeTranscriptApi
from mongodb.mongodb import MongoDBClient

def get_playlist_video_urls(playlist_url):
    playlist = Playlist(playlist_url)

    video_urls = list(playlist.url_generator())
    return video_urls


def process_videos_by_video_urls(video_urls: [str]) -> None:
    try:
        for url in video_urls:
            process_single_video(url)
    except Exception as e:
        print(f"Error on process_videos_by_channel_url: {str(e)}")


def process_single_video(video_url: str) -> None:
    try:
        print(f"Processing video {video_url}")
        video_data: Dict[str, Any] = extract_video_data_by_video_url(video_url)

        video_id: str = video_data["infos"]["videoId"]

        mongo_client_for_transcriptions: MongoDBClient = MongoDBClient(
            collection_name="videoData"
        )
        mongo_client_for_transcriptions.insert_document(
            document=video_data["infos"], document_id=video_id
        )

        mongo_client_for_video_data: MongoDBClient = MongoDBClient(
            collection_name="videoTranscriptions"
        )
        mongo_client_for_video_data.insert_document(
            document=video_data["transcript"], document_id=video_id
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

        return {
            "infos": {
                **youtube_video.vid_info["videoDetails"],
                "watchUrl": youtube_video.watch_url,
                "videoId": video_id,
            },
            "transcript": {
                "transcript": transcript[0][youtube_video.video_id],
            },
        }
    except Exception as e:
        print(f"Error extracting data for video {video_url}: {str(e)}")

