import re
from dataclasses import asdict
from .schema import Episode, Scene
from .ai_content import generate_ai_content

DEFAULT_LOCATIONS = [
    "colorful_classroom",
    "alphabet_garden",
    "sunny_playground",
    "rainbow_park",
    "cozy_library",
]
DEFAULT_ACTIONS = ["enter", "wave", "point", "clap", "dance", "celebrate"]

def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "episode"

def generate_episode(topic, duration=30, characters=None, ai=True):
    topic = topic.strip()
    if not topic:
        raise ValueError("topic is required")
    duration = float(duration)
    if duration < 6:
        raise ValueError("duration must be at least 6 seconds")
    characters = characters or ["child_01", "child_02", "friendly_dog"]
    n = 3
    base = duration / n
    ai_data = generate_ai_content(topic, duration) if ai else {}
    ai_scenes = ai_data.get("scenes", [])
    scenes = []
    for i in range(n):
        src = ai_scenes[i] if i < len(ai_scenes) else {}
        scenes.append(Scene(
            location=src.get("location", DEFAULT_LOCATIONS[i % len(DEFAULT_LOCATIONS)]),
            duration=base,
            actions=src.get("actions", DEFAULT_ACTIONS[i*2:i*2+3]),
            characters=list(characters),
            voice=src.get("voice", ""),
            visual_prompt=src.get("visual_prompt", ""),
        ))
    return Episode(
        title=ai_data.get("title", f"{topic.title()} Adventure"),
        duration=duration,
        style="original_preschool_3d",
        characters=list(characters),
        scenes=scenes,
        metadata={
            "topic": topic,
            "slug": slug(topic),
            "audience": "preschool",
            "language": "en",
            "content_type": "educational_3d_animation",
            "originality": "original_characters_and_story",
            "learning_goal": ai_data.get("learning_goal", ""),
            "lyrics": ai_data.get("lyrics", ""),
            "narration": ai_data.get("narration", []),
        },
    )

def episode_dict(ep):
    data = asdict(ep)
    return data
