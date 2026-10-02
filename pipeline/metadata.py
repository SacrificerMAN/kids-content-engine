import json
from pathlib import Path

def build_metadata(episode):
    topic = episode.metadata.get("topic", episode.title)
    tags = ["preschool", "kids learning", "3d animation", "educational", topic.lower()]
    return {
        "title": episode.title,
        "description": (
            f"An original preschool 3D adventure about {topic}. "
            "Created with original characters and an original story concept."
        ),
        "tags": tags,
        "category": "Education",
        "audience": "preschool",
        "language": episode.metadata.get("language", "en"),
        "thumbnail_text": topic.title(),
    }

def write_metadata(path, episode):
    Path(path).write_text(json.dumps(build_metadata(episode), indent=2), encoding="utf-8")
    return str(path)
