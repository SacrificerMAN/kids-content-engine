from pipeline.tts import synthesize
from pipeline.music import create_music_bed

def test_local_tts_provider(monkeypatch, tmp_path):
    monkeypatch.setenv("TTS_PROVIDER","local")
    import pipeline.tts as t
    target=tmp_path/"voice.m4a"
    monkeypatch.setattr(t,"_local_tts",lambda text,out: str(out))
    assert t.synthesize("hello",target).endswith("voice.m4a")

def test_music_function_exists():
    assert callable(create_music_bed)
