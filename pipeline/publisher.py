import os
from dataclasses import dataclass
from .publishing import publish as publish_real, PublishingError

@dataclass
class PublishResult:
    platform:str
    status:str
    detail:str
    url:str|None=None

class Publisher:
    def __init__(self,dry_run=True):
        self.dry_run=dry_run

    def publish(self,video_path,title,description='',platforms=None,privacy=None):
        privacy=privacy or os.getenv("PUBLISH_PRIVACY","private")
        return [self._one(p,video_path,title,description,privacy) for p in (platforms or ["youtube"])]

    def _one(self,platform,video_path,title,description,privacy):
        if self.dry_run or os.getenv("PUBLISH_ENABLED","0")!="1":
            return PublishResult(platform,"dry_run","publishing is disabled")
        try:
            data=publish_real(platform,video_path,title,description,privacy)
            url=None
            if platform=="youtube" and data.get("id"):
                url=f"https://www.youtube.com/watch?v={data['id']}"
            return PublishResult(platform,"published",f"{platform} upload completed",url)
        except (PublishingError, OSError, ValueError) as exc:
            return PublishResult(platform,"failed",str(exc))
