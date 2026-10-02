from pipeline.ai_content import generate_ai_content

def test_ai_content_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    data=generate_ai_content("colors",30)
    assert data["title"]
    assert len(data["scenes"])==3
    assert data["lyrics"]
