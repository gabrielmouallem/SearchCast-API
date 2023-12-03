import os
from api.common.services.processor.processor_service import VideoProcessingService
from config.setup import setup

setup()

mongo_uri = os.environ.get("MONGO_URI")

playlist_urls = [
    "https://www.youtube.com/watch?v=RGRPikhvsfw&list=PLWieWKZeFoVQBl5jPTEvWUah6-FTufaKi",
    "https://www.youtube.com/watch?v=Po-ja6buGy4&list=PLWieWKZeFoVRmUNn9KA2dVpQswo19QkwQ",
    "https://www.youtube.com/watch?v=deKKy5uzPaU&list=PLJznpI7w9TooV0ORuL9e4ZRYMznV_Dwdp",
    "https://www.youtube.com/watch?v=PBWYMa3nuiw&list=PLaE_mZALZ0V2E0lVJowee_oerd3OMvyJu",
    "https://www.youtube.com/watch?v=n-53I1tfnIw&list=PLczDDIRnclWRAi9rLUxxUHz2j7XSEothf",
    "https://www.youtube.com/watch?v=8Bkl7KEbw2Q&list=PLByCI4BxQvkSJKS_sj01Vg_5kuyBO3bsq",
]


# def start(url: str):
def start():
    confirmation = input("Are you sure (yes/no) ? Remember the billing costs! ")
    if str(confirmation) == "yes":
        print("Okay, here we go...")
    try:
        VideoProcessingService(mongo_uri=mongo_uri).process_by_playlist_urls(
            playlist_urls=playlist_urls, max_videos_per_channel=20
        )
    except Exception as ex:
        print(str(ex))


# link = input("Enter the YouTube playlist URL: ")
# start(link)
start()
