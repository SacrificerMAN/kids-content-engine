from pipeline.content_generator import generate_episode
from pipeline.metadata import build_metadata
from pipeline.topic_pipeline import create_topic_package

def test_topic_generates_valid_episode(tmp_path):
    ep=generate_episode("colors",duration=30)
    assert ep.title == "Colors Adventure"
    assert sum(s.duration for s in ep.scenes) == 30
    assert ep.style == "original_preschool_3d"

def test_metadata_is_original():
    ep=generate_episode("animals")
    meta=build_metadata(ep)
    assert "Original" in meta["description"]
    assert "preschool" in meta["tags"]

def test_topic_package(tmp_path):
    result=create_topic_package("letters",tmp_path)
    assert result["episode"].endswith("episode.json")
    assert result["metadata"].endswith("metadata.json")
    assert result["thumbnail"].endswith("thumbnail.svg")
