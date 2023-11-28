import os
from api.common.services.processor.processor_service import VideoProcessingService
from config.setup import setup

setup()

mongo_uri = os.environ.get("MONGO_URI")

playlist_urls = [
    "https://www.youtube.com/watch?v=0Llr0TcF_sk&list=PLWieWKZeFoVRmUNn9KA2dVpQswo19QkwQ&pp=iAQB",
]


# def start(url: str):
def start():
    confirmation = input("Are you sure (yes/no) ? Remember the billing costs! ")
    if str(confirmation) == "yes":
        print("Okay, here we go...")
        try:
            VideoProcessingService(mongo_uri=mongo_uri).process_by_playlist_urls(
                playlist_urls=playlist_urls, max_videos_per_channel=9999
            )
        except Exception as ex:
            print(str(ex))
    else:
        return


# link = input("Enter the YouTube playlist URL: ")
# start(link)
start()
