import os, requests
from pathlib import Path

class PublishingError(RuntimeError): pass

def youtube_upload(video_path,title,description,privacy="private"):
    token=os.getenv("YOUTUBE_ACCESS_TOKEN")
    if not token: raise PublishingError("YOUTUBE_ACCESS_TOKEN not configured")
    size=Path(video_path).stat().st_size
    headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"}
    metadata={"snippet":{"title":title,"description":description,"categoryId":"27"},"status":{"privacyStatus":privacy}}
    init=requests.post("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                       headers=headers,json=metadata,timeout=60)
    init.raise_for_status()
    upload_url=init.headers.get("Location")
    if not upload_url: raise PublishingError("YouTube did not return resumable upload URL")
    with open(video_path,"rb") as fh:
        put=requests.put(upload_url,headers={"Content-Type":"video/mp4","Content-Length":str(size)},
                         data=fh,timeout=3600)
    put.raise_for_status()
    return put.json()

def publish(platform,video_path,title,description,privacy="private"):
    if platform=="youtube": return youtube_upload(video_path,title,description,privacy)
    raise PublishingError(f"{platform} adapter is not configured yet")
