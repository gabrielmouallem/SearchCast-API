import os
from pytube import YouTube


def on_progress(stream, chunk, remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Downloading... {percentage:.2f}% complete", end="\r")


def download(link):
    try:
        youtube_object = YouTube(link, on_progress_callback=on_progress)
        video_stream = youtube_object.streams.get_highest_resolution()

        # Create a 'videos' folder if it doesn't exist
        if not os.path.exists("videos"):
            os.makedirs("videos")

        # Set the download path to the 'videos' folder with the original video name
        download_path = os.path.join("videos", video_stream.default_filename)
        video_stream.download(output_path=".", filename=download_path)

        print("\nDownload is completed successfully")

    except Exception as e:
        print(f"\nAn error has occurred: {e}")


if __name__ == "__main__":
    link = input("Enter the YouTube video URL: ")
    download(link)
