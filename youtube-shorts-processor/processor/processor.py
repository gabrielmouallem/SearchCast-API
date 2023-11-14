from pytube import YouTube
from scripts.utils import get_size_in_mb
from youtube_transcript_api import YouTubeTranscriptApi

def extract_captions(video_url):
    # Create a YouTube object
    youtube_video_data = YouTube(video_url)
    youtube_video_data_size = get_size_in_mb(youtube_video_data)
    print(f"youtube_video_data_size: {youtube_video_data_size} MB")
    video_id = [youtube_video_data.video_id]    
    
    transcript = YouTubeTranscriptApi.get_transcripts(video_id, languages=['pt', 'en'])
    transcript_size = get_size_in_mb(transcript)
    print(f"transcript_size: {transcript_size} MB")
    
    # print(transcript)
    
    
