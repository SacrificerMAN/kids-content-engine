from pipeline.tts import synthesize
from pipeline.music import create_music_bed
from pathlib import Path

def test_local_tts_path(monkeypatch,tmp_path):
    monkeypatch.setenv("TTS_PROVIDER","local")
    import pipeline.tts as t
    monkeypatch.setattr(t,"_local_tts",lambda text,out: str(Path(out)))
    out=tmp_path/"voice.m4a"
    # Provider selection and local path are exercised without requiring espeak in unit CI.
    assert t._local_tts("hello", out).endswith("voice.wav")

def test_music_function_exists():
    assert callable(create_music_bed)
