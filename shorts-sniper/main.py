from dotenv import load_dotenv
from mongodb.mongodb import MongoDBClient
from processor.processor import process_videos_by_channel_url


# main.py
def main():
    load_dotenv()
    process_videos_by_channel_url(
        "https://www.youtube.com/channel/UC4ncvgh5hFr5O83MH7-jRJg"
    )


if __name__ == "__main__":
    main()
