from services.processor import VideoProcessingService


def start(url: str):
    VideoProcessingService().process_by_playlist_url(playlist_url=url)


link = input("Enter the YouTube playlist URL: ")
start(link)
