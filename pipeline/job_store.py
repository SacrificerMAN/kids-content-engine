import json, time, uuid
from pathlib import Path

class JobStore:
    def __init__(self, root):
        self.root=Path(root)/"jobs"; self.root.mkdir(parents=True,exist_ok=True)
    def create(self, payload):
        job_id=uuid.uuid4().hex
        data={"id":job_id,"created_at":time.time(),"status":"queued","request":payload}
        (self.root/f"{job_id}.json").write_text(json.dumps(data,indent=2),encoding="utf-8")
        return data
    def update(self,job_id,**changes):
        p=self.root/f"{job_id}.json"
        data=json.loads(p.read_text(encoding="utf-8")); data.update(changes)
        p.write_text(json.dumps(data,indent=2),encoding="utf-8"); return data
    def get(self,job_id):
        p=self.root/f"{job_id}.json"
        if not p.exists(): return None
        return json.loads(p.read_text(encoding="utf-8"))
