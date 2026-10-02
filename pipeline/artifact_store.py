import os, shutil
from pathlib import Path

class ArtifactStore:
    def __init__(self, root=None):
        self.root=Path(root or os.getenv("ARTIFACT_ROOT","/tmp/kids-artifacts"))
        self.root.mkdir(parents=True,exist_ok=True)
    def put(self,path,key=None):
        src=Path(path)
        if not src.exists(): raise FileNotFoundError(path)
        dest=self.root/(key or src.name)
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dest)
        return {"backend":"local","path":str(dest),"size":dest.stat().st_size}
