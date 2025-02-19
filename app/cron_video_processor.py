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
    # New URLs
    "https://www.youtube.com/watch?v=_yp18pX_3NQ&list=PLWieWKZeFoVQBl5jPTEvWUah6-FTufaKi&pp=iAQB",
    "https://www.youtube.com/watch?v=NxlFkOCwlaw&list=PLV-b4RRsU-VYG_8VTZAmoETlHwd1s9LHg",
    "https://www.youtube.com/watch?v=RYexfrU07B8&list=PLV-b4RRsU-VbpgVwNbXEm_961lSwZii7j",
    "https://www.youtube.com/watch?v=rnZn62458Dc&list=PLk_e6laOs_lRUrOG0x9Ba5S5QsVdVqb2J&pp=iAQB",
    "https://www.youtube.com/watch?v=jhSeRasb1Lw&list=PLlHCt9SnkpCjUzX-cFQLuo6MI6-eSxFOw",
    "https://www.youtube.com/watch?v=wWCr2p0PIh4&list=PLW3mXBgY1SKXqrcDlApx2Xntuyl_J1zpe",
    "https://www.youtube.com/watch?v=SQsI_KtC3JE&list=PLtyaItn7iHcuwMma-Frjq28JsPVklxPBp",
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
