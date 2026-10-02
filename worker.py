import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline.orchestrator import Orchestrator

app=FastAPI(title="Kids Content Engine",version="1.0.0")
ROOT=Path(os.getenv("WORK_ROOT","/tmp/kids-content-engine")); ROOT.mkdir(parents=True,exist_ok=True)
class RenderJob(BaseModel):
    episode:str
    publish:bool=False
    dry_run:bool=True

def safe_episode(path:str):
    p=Path(path)
    if p.is_absolute() or ".." in p.parts: raise HTTPException(400,"invalid episode path")
    candidate=(Path.cwd()/p).resolve()
    if not candidate.is_file(): raise HTTPException(404,"episode not found")
    return str(candidate)

@app.get("/health")
def health(): return {"status":"ok","service":"kids-content-engine","render_enabled":os.getenv("RENDER_ENABLED","0")}

@app.get("/")
def root(): return {"service":"kids-content-engine","status":"ready","version":"1.0.0"}

@app.post("/jobs")
def create_job(job:RenderJob): return {"status":"accepted","episode":job.episode,"publish":job.publish,"dry_run":job.dry_run}

@app.post("/run")
def run_job(job:RenderJob):
    episode=safe_episode(job.episode)
    if job.publish and os.getenv("PUBLISH_ENABLED","0")!="1": raise HTTPException(403,"publishing disabled")
    try: return {"status":"completed","result":Orchestrator(str(ROOT)).run(episode,publish=job.publish,dry_run=job.dry_run)}
    except Exception as exc: raise HTTPException(500,str(exc))
