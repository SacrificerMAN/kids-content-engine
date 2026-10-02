from pathlib import Path

def validate_render(path):
    p = Path(path)
    if not p.exists():
        return {"ok":False,"error":"file_not_found"}
    if p.stat().st_size == 0:
        return {"ok":False,"error":"empty_file"}
    return {"ok":True,"size":p.stat().st_size}