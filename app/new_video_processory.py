from services.processor.processor_service import VideoProcessingService

playlist_urls = []


# def start(url: str):
def start():
    confirmation = input("Are you sure (yes/no) ? Remember the billing costs! ")
    if str(confirmation) == "yes":
        print("Okay, here we go...")
        VideoProcessingService().process_by_playlist_urls(
            playlist_urls=playlist_urls, max_videos_per_channel=9999
        )
    else:
        return


# link = input("Enter the YouTube playlist URL: ")
# start(link)
start()
