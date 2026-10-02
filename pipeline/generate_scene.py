import json
from pathlib import Path

def load_episode(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def build_manifest(path):
    episode = load_episode(path)
    return {
        "title": episode["title"],
        "duration": episode["duration"],
        "scenes": episode["scenes"],
        "characters": episode.get("characters", [])
    }

if __name__ == "__main__":
    print(json.dumps(build_manifest("content/demo_episode.json"), indent=2))