import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Kids Content Engine")
ROOT = Path(os.getenv("WORK_ROOT","/tmp/kids-content-engine"))
ROOT.mkdir(parents=True, exist_ok=True)

class RenderJob(BaseModel):
    episode: str
    publish: bool = False

@app.get("/health")
def health():
    return {"status":"ok","service":"kids-content-engine"}

@app.post("/jobs")
def create_job(job: RenderJob):
    episode = Path(job.episode)
    if episode.is_absolute() or ".." in episode.parts:
        raise HTTPException(400,"invalid episode path")
    return {"status":"accepted","episode":str(episode),"publish":job.publish}

@app.get("/")
def root():
    return {"service":"kids-content-engine","status":"ready"}