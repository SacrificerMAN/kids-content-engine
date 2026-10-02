import os
from pathlib import Path

class ArtifactStore:
    def __init__(self, root=None):
        self.root=Path(root or os.getenv("ARTIFACT_ROOT","/tmp/kids-artifacts"))
        self.root.mkdir(parents=True,exist_ok=True)
    def put(self,path):
        src=Path(path)
        if not src.exists(): raise FileNotFoundError(path)
        dest=self.root/src.name
        dest.write_bytes(src.read_bytes())
        return {"backend":"local","path":str(dest),"size":dest.stat().st_size}
