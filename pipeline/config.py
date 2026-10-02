import os

def env(name: str, default=None):
    return os.getenv(name, default)

CONFIG = {
    "youtube_token": env("YOUTUBE_ACCESS_TOKEN"),
    "facebook_token": env("FACEBOOK_ACCESS_TOKEN"),
    "instagram_token": env("INSTAGRAM_ACCESS_TOKEN"),
}