import os
import youtube_dl


def download(link):
    try:
        options = {
            "outtmpl": os.path.join("videos", "%(title)s.%(ext)s"),
            "progress_hooks": [on_progress],
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([link])

        print("\nDownload is completed successfully")

    except Exception as e:
        print(f"\nAn error has occurred: {e}")


def on_progress(d):
    if d["status"] == "finished":
        print("\nDownload completed successfully")
    else:
        total_size = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
        downloaded_bytes = d.get("downloaded_bytes", 0)
        percentage = (downloaded_bytes / total_size) * 100
        print(f"Downloading... {percentage:.2f}% complete", end="\r")


if __name__ == "__main__":
    link = input("Enter the YouTube video URL: ")
    download(link)
