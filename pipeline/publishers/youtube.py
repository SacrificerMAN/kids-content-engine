import os, requests

class YouTubePublisher:
    def __init__(self):
        self.token=os.getenv("YOUTUBE_ACCESS_TOKEN")
    def upload(self, video_path, title, description=""):
        if not self.token: return {"status":"disabled","reason":"YOUTUBE_ACCESS_TOKEN missing"}
        # OAuth token is accepted, but upload is deliberately gated by an explicit flag.
        if os.getenv("YOUTUBE_UPLOAD_ENABLED","0")!="1":
            return {"status":"disabled","reason":"YOUTUBE_UPLOAD_ENABLED is not 1"}
        url="https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status&uploadType=media"
        headers={"Authorization":f"Bearer {self.token}","Content-Type":"video/mp4"}
        metadata={"snippet":{"title":title,"description":description},"status":{"privacyStatus":os.getenv("YOUTUBE_PRIVACY","private")}}
        # Use multipart upload so metadata and media are sent together.
        files={"media":("video.mp4",open(video_path,"rb"),"video/mp4")}
        data={"snippet":__import__("json").dumps(metadata["snippet"]),"status":__import__("json").dumps(metadata["status"])}
        r=requests.post(url,headers=headers,data=data,files=files,timeout=1800)
        r.raise_for_status()
        return {"status":"uploaded","response":r.json()}
