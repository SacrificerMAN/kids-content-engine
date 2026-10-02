import os
from .publishers.youtube import YouTubePublisher

def publish(video_path,title,description="",platforms=None):
    platforms=platforms or ["youtube"]
    results=[]
    for platform in platforms:
        if platform=="youtube":
            results.append({"platform":"youtube","result":YouTubePublisher().upload(video_path,title,description)})
        else:
            results.append({"platform":platform,"result":{"status":"disabled","reason":"adapter not configured"}})
    return results
