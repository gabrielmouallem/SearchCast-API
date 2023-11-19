from dotenv import load_dotenv
from processor.processor_v2 import get_playlist_video_urls, process_videos_by_video_urls

# (check) https://www.youtube.com/watch?v=Cko3pI9ulo4&list=PLWieWKZeFoVSLVo0Bn5UdlUdsuz21CXcF
# https://www.youtube.com/watch?v=gXfVH25EbJ8&list=PLWieWKZeFoVRmUNn9KA2dVpQswo19QkwQ
# https://www.youtube.com/watch?v=_UFCNsVBVtA&list=PLaE_mZALZ0V2E0lVJowee_oerd3OMvyJu
# https://www.youtube.com/watch?v=eG5GrTqyGBQ&list=PLJznpI7w9TooV0ORuL9e4ZRYMznV_Dwdp

# main.py
def main():
    load_dotenv()

    all_urls = []  # Create an empty list to store all URLs
    
    urls = get_playlist_video_urls("https://www.youtube.com/watch?v=Cko3pI9ulo4&list=PLWieWKZeFoVSLVo0Bn5UdlUdsuz21CXcF")
    all_urls.extend(urls)  # Append URLs to the list

    urls = get_playlist_video_urls("https://www.youtube.com/watch?v=gXfVH25EbJ8&list=PLWieWKZeFoVRmUNn9KA2dVpQswo19QkwQ")
    all_urls.extend(urls)  # Append URLs to the list

    urls = get_playlist_video_urls("https://www.youtube.com/watch?v=_UFCNsVBVtA&list=PLaE_mZALZ0V2E0lVJowee_oerd3OMvyJu")
    all_urls.extend(urls)  # Append URLs to the list

    urls = get_playlist_video_urls("https://www.youtube.com/watch?v=eG5GrTqyGBQ&list=PLJznpI7w9TooV0ORuL9e4ZRYMznV_Dwdp")
    all_urls.extend(urls)  # Append URLs to the list

    # Now, 'all_urls' contains all the concatenated URLs
    process_videos_by_video_urls(all_urls)


if __name__ == "__main__":
    main()
