from dotenv import load_dotenv
from processor.processor_v2 import get_playlist_video_urls, process_videos_by_video_urls

# (check) https://www.youtube.com/watch?v=Cko3pI9ulo4&list=PLWieWKZeFoVSLVo0Bn5UdlUdsuz21CXcF
# https://www.youtube.com/watch?v=gXfVH25EbJ8&list=PLWieWKZeFoVRmUNn9KA2dVpQswo19QkwQ
# https://www.youtube.com/watch?v=_UFCNsVBVtA&list=PLaE_mZALZ0V2E0lVJowee_oerd3OMvyJu
# https://www.youtube.com/watch?v=eG5GrTqyGBQ&list=PLJznpI7w9TooV0ORuL9e4ZRYMznV_Dwdp

# main.py
def main():
    load_dotenv()
    
    urls = get_playlist_video_urls("https://www.youtube.com/watch?v=Cko3pI9ulo4&list=PLWieWKZeFoVSLVo0Bn5UdlUdsuz21CXcF")
    process_videos_by_video_urls(urls)
    
    urls = get_playlist_video_urls("https://www.youtube.com/watch?v=gXfVH25EbJ8&list=PLWieWKZeFoVRmUNn9KA2dVpQswo19QkwQ")
    process_videos_by_video_urls(urls)
    
    urls = get_playlist_video_urls("https://www.youtube.com/watch?v=_UFCNsVBVtA&list=PLaE_mZALZ0V2E0lVJowee_oerd3OMvyJu")
    process_videos_by_video_urls(urls)
    
    urls = get_playlist_video_urls("https://www.youtube.com/watch?v=eG5GrTqyGBQ&list=PLJznpI7w9TooV0ORuL9e4ZRYMznV_Dwdp")
    process_videos_by_video_urls(urls)


if __name__ == "__main__":
    main()
