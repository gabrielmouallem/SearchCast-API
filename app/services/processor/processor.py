from typing import Dict, Any
from pytube import YouTube, Playlist, Channel
from youtube_transcript_api import YouTubeTranscriptApi
from utils import generate_unique_id, extract_video_id
from services.mongodb import MongoDBClientService
import time


class VideoProcessingService:
    def __init__(self):
        self.transcriptions_collection = "videoData"
        self.video_transcriptions_collection = "videoTranscriptions"

    def get_channel_video_urls(self, channel_url: str):
        channel = Channel(channel_url)

        video_urls = list(channel.url_generator())
        return video_urls

    def process_by_channel_url(self, channel_url: str):
        video_urls = self.get_channel_video_urls(channel_url=channel_url)
        self.process_by_video_urls(video_urls=video_urls)

    def process_by_playlist_urls(self, playlist_urls: [str]):
        for playlist_url in playlist_urls:
            self.process_by_playlist_url(playlist_url=playlist_url)

    def get_playlist_video_urls(self, playlist_url: str):
        playlist = Playlist(playlist_url)

        video_urls = list(playlist.url_generator())
        return video_urls

    def process_by_playlist_url(self, playlist_url: str):
        video_urls = self.get_playlist_video_urls(playlist_url=playlist_url)
        self.process_by_video_urls(video_urls=video_urls)

    def process_by_video_urls(self, video_urls: [str]) -> None:
        total_videos = len(video_urls)
        video_processed_count = 0
        start_time = time.time()

        for url in video_urls:
            is_processed = self._check_if_video_is_already_processed(url)
            # print(f"Video {url} already processed")
            if is_processed is False:
                self.process_single_video(url)
            video_processed_count += 1
            self._print_progress(video_processed_count, total_videos, start_time)

    def process_single_video(self, video_url: str) -> None:
        video_data = self.extract_video_data_by_video_url(video_url)
        video_id = video_data["infos"]["videoId"]

        self._save_video_data_to_mongo(
            video_data["infos"], video_id, self.transcriptions_collection
        )

        transcripts = video_data["transcript"]
        self._save_transcripts_to_mongo(
            transcripts, video_data["infos"], self.video_transcriptions_collection
        )
        # print(f"Video {video_url} processed")

        # print(f"Error processing video {video_url}: {str(e)}")

    def extract_video_data_by_video_url(
        self, video_url: str
    ) -> Dict[str, Dict[str, Any]]:
        try:
            youtube_video = YouTube(video_url)
            video_id = youtube_video.video_id

            transcript = YouTubeTranscriptApi.get_transcripts(
                [video_id], languages=["pt", "en"]
            )
            transcript_array = transcript[0][video_id]

            return {
                "infos": {
                    **youtube_video.vid_info["videoDetails"],
                    "publishDate": youtube_video.publish_date,
                    "watchUrl": youtube_video.watch_url,
                    "videoId": video_id,
                },
                "transcript": transcript_array,
            }

        except Exception as e:
            pass
            # print(f"Error extracting data for video {video_url}: {str(e)}")

    def _check_if_video_is_already_processed(self, video_url: str):
        mongo_client = MongoDBClientService(collection_name="videoData")
        video_id = extract_video_id(video_url)
        if video_id is None:
            return False
        video = mongo_client.find_document(video_id)
        if video is None:
            return False
        else:
            return True

    def _save_video_data_to_mongo(
        self, document: Dict[str, Any], document_id: str, collection_name: str
    ) -> None:
        mongo_client = MongoDBClientService(collection_name=collection_name)
        mongo_client.insert_document(document=document, document_id=document_id)

    def _save_transcripts_to_mongo(
        self, transcripts: [dict], video_data: dict, collection_name: str
    ) -> None:
        mongo_client = MongoDBClientService(collection_name=collection_name)
        for transcript_entry in transcripts:
            transcript_document = {**transcript_entry, "video": video_data}
            id = generate_unique_id(transcript_document)
            mongo_client.insert_document(document=transcript_document, document_id=id)

    def _print_progress(
        self, processed_count: int, total: int, start_time: float
    ) -> None:
        elapsed_time = time.time() - start_time
        average_time_per_video = elapsed_time / processed_count
        remaining_videos = total - processed_count
        estimated_remaining_time = remaining_videos * average_time_per_video
        remaining_time_str = time.strftime(
            "%H:%M", time.gmtime(estimated_remaining_time)
        )

        print(
            f"Processed {processed_count}/{total} videos | Estimated remaining time: {remaining_time_str}",
            end="\r",
            flush=True,
        )
