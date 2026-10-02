from pathlib import Path
from .content_generator import generate_episode
from .metadata import write_metadata
from .thumbnail import create_thumbnail_svg

def create_topic_package(topic, root, duration=30):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    ep = generate_episode(topic, duration=duration)
    slug = ep.metadata["slug"]
    job = root / slug
    job.mkdir(parents=True, exist_ok=True)
    episode_path = job / "episode.json"
    metadata_path = job / "metadata.json"
    thumb_path = job / "thumbnail.svg"
    import json
    episode_path.write_text(json.dumps({
        "title": ep.title,
        "duration": ep.duration,
        "style": ep.style,
        "characters": ep.characters,
        "scenes": [s.__dict__ for s in ep.scenes],
        "metadata": ep.metadata
    }, indent=2), encoding="utf-8")
    write_metadata(metadata_path, ep)
    create_thumbnail_svg(thumb_path, ep.title)
    return {
        "episode": str(episode_path),
        "metadata": str(metadata_path),
        "thumbnail": str(thumb_path),
        "title": ep.title,
        "slug": slug,
    }
