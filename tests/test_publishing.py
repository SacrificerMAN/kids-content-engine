from pipeline.publisher import Publisher

def test_publishing_is_gated(monkeypatch,tmp_path):
    monkeypatch.setenv("PUBLISH_ENABLED","0")
    result=Publisher(dry_run=False).publish(str(tmp_path/"x.mp4"),"Test","Desc")
    assert result[0].status=="dry_run"
