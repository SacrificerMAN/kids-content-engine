from dataclasses import dataclass, field
from pathlib import Path
import json

@dataclass
class Scene:
    location: str
    duration: float
    actions: list[str] = field(default_factory=list)
    characters: list[str] = field(default_factory=list)
    voice: str = ""
    visual_prompt: str = ""

@dataclass
class Episode:
    title: str
    duration: float
    style: str = "original_preschool_3d"
    characters: list[str] = field(default_factory=list)
    scenes: list[Scene] = field(default_factory=list)
    audio: str | None = None
    metadata: dict = field(default_factory=dict)

def load_episode(path: str) -> Episode:
    raw=json.loads(Path(path).read_text(encoding="utf-8"))
    ep=Episode(title=raw["title"],duration=float(raw["duration"]),style=raw.get("style","original_preschool_3d"),characters=raw.get("characters",[]),scenes=[Scene(**s) for s in raw.get("scenes",[])],audio=raw.get("audio"),metadata=raw.get("metadata",{}))
    if ep.duration <= 0 or not ep.scenes: raise ValueError("episode needs positive duration and scenes")
    if abs(sum(s.duration for s in ep.scenes)-ep.duration) > 0.25: raise ValueError("scene durations must equal episode duration")
    return ep
