import os
from api.common.services.processor.processor_service import VideoProcessingService
from config.setup import setup

setup()

mongo_uri = os.environ.get("MONGO_URI")

# https://www.youtube.com/podcasts/popularshows

playlist_urls = [
    "https://www.youtube.com/watch?v=deKKy5uzPaU&list=PLJznpI7w9TooV0ORuL9e4ZRYMznV_Dwdp",
    "https://www.youtube.com/watch?v=6gqjTv8AzOw&list=PLV-b4RRsU-VYLTSoqXz9J2abV2-MWh6eq",
    "https://www.youtube.com/watch?v=deKKy5uzPaU&list=PLJznpI7w9TooV0ORuL9e4ZRYMznV_Dwdp",
    "https://www.youtube.com/watch?v=Po-ja6buGy4&list=PLWieWKZeFoVRmUNn9KA2dVpQswo19QkwQ",
    "https://www.youtube.com/watch?v=PBWYMa3nuiw&list=PLaE_mZALZ0V2E0lVJowee_oerd3OMvyJu",
    "https://www.youtube.com/watch?v=u3jjwO0egAM&list=PLk_e6laOs_lSC7O_qcR9vgBg_EVvVSF33",
    "https://www.youtube.com/watch?v=8Bkl7KEbw2Q&list=PLByCI4BxQvkSJKS_sj01Vg_5kuyBO3bsq",
    "https://www.youtube.com/watch?v=WqiLEK-Lzw4&list=PLWBcDIDlsDmq6o7Qvyn_NfHcKpLYgrjI8",
    "https://www.youtube.com/watch?v=ObdvuVmYOy4&list=PLkKsdR0a6X5Qz26LZ20WcukTWbNUVXAVN",
    "https://www.youtube.com/watch?v=9JyRGOiBt0o&list=PL2LH9u21t_RQC1viFOKJOvUa9aPwi9Aez",
    "https://www.youtube.com/watch?v=n-53I1tfnIw&list=PLczDDIRnclWRAi9rLUxxUHz2j7XSEothf",
    "https://www.youtube.com/watch?v=1oEaEB0j3bc&list=PLap7g1BFssvl6xYS8OyNk4JvJBMUeEKfo",
]


# def start(url: str):
def start():
    try:
        VideoProcessingService(mongo_uri=mongo_uri).process_by_playlist_urls(
            playlist_urls=playlist_urls, max_videos_per_channel=20
        )
    except Exception as ex:
        print(str(ex))


# link = input("Enter the YouTube playlist URL: ")
# start(link)
start()
