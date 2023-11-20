# routes.py
from flask import jsonify, request
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.shortsSniper

"""

videoTranscriptions collection data format:

{
  "_id": "cc94950c52b5d7be6c6201db62a7190a",
  "text": "estamos começando mais um flor eu sou",
  "start": 30.96,
  "duration": 4.56,
  "videoId": "Cko3pI9ulo4" --> This videoId is the _id of the videoData collection
}

videoData collection data format:

{
  "_id": "Cko3pI9ulo4",
  "videoId": "Cko3pI9ulo4",
  "title": "POPÓ - Flow Podcast #544 🤝 @FlowSportClub",
  "lengthSeconds": "9567",
  "channelId": "UC4ncvgh5hFr5O83MH7-jRJg",
  "isOwnerViewing": false,
  "isCrawlable": true,
  "thumbnail": {
    "thumbnails": [
      {
        "url": "https://i.ytimg.com/vi/Cko3pI9ulo4/mqdefault.jpg?v=61fc67ad",
        "width": 320,
        "height": 180
      },
      {
        "url": "https://i.ytimg.com/vi/Cko3pI9ulo4/hqdefault.jpg?sqp=-oaymwEXCJADEOABSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLAM4U1DnJJiofKfPE8T-I8zqsoDSA",
        "width": 400,
        "height": 224
      },
      {
        "url": "https://i.ytimg.com/vi/Cko3pI9ulo4/hq720.jpg?sqp=-oaymwEXCKAGEMIDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLCkOyE2gIVVRtnXVLYl3Zs8KPKmEA",
        "width": 800,
        "height": 450
      },
      {
        "url": "https://i.ytimg.com/vi/Cko3pI9ulo4/hq720.jpg?v=61fc67ad",
        "width": 1280,
        "height": 720
      }
    ]
  },
  "allowRatings": true,
  "viewCount": "1369209",
  "author": "Flow Podcast 1.0 - Episódios Completos",
  "isLowLatencyLiveStream": false,
  "isPrivate": false,
  "isUnpluggedCorpus": false,
  "latencyClass": "MDE_STREAM_OPTIMIZATIONS_RENDERER_LATENCY_NORMAL",
  "musicVideoType": "MUSIC_VIDEO_TYPE_PODCAST_EPISODE",
  "isLiveContent": true,
  "watchUrl": "https://youtube.com/watch?v=Cko3pI9ulo4"
}

"""


def configure_routes(app):
    @app.route("/videoData", methods=["GET"])
    def get_all_video_data():
        videoDatas = db.videoData.find()
        return jsonify([data for data in videoDatas])

    @app.route("/videoData/<int:id>", methods=["GET"])
    def get_video_data_by_id(id):
        videoData = db.videoData.find_one({"_id": id})
        return videoData

    @app.route("/search", methods=["GET"])
    def search_transcriptions():
        query_text = request.args.get("text", "")

        # Perform case-insensitive regex search on the 'text' field
        regex_query = {"text": {"$regex": f".*{query_text}.*", "$options": "i"}}

        # Aggregation pipeline to join videoData with matching videoTranscriptions
        aggregation_pipeline = [
            {"$match": regex_query},
            {
                "$lookup": {
                    "from": "videoData",
                    "localField": "videoId",
                    "foreignField": "_id",
                    "as": "videoData",
                }
            },
            {"$unwind": "$videoData"},
            {"$project": {"_id": 0, "transcription": "$$ROOT"}},
        ]

        # Execute the aggregation pipeline
        aggregated_data = list(db.videoTranscriptions.aggregate(aggregation_pipeline))

        return jsonify(aggregated_data)
