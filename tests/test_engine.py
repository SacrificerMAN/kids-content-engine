from pipeline.schema import load_episode
from pipeline.audio_sync import distribute_audio

def test_episode_schema():
    ep=load_episode('content/demo_episode.json'); assert ep.duration==30; assert len(ep.scenes)==3

def test_audio_distribution():
    assert distribute_audio(30,[10,10,10])==[10.0,10.0,10.0]
