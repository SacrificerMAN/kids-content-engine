import json
from pathlib import Path
from datetime import datetime, timezone

def write_production_manifest(job_dir, **data):
    payload={"created_at":datetime.now(timezone.utc).isoformat(),"version":"3.0.0",**data}
    path=Path(job_dir)/"production.json"
    path.write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding="utf-8")
    return str(path)
