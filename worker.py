import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks\nfrom fastapi.responses import FileResponse
from pydantic import BaseModel
from pipeline.orchestrator import Orchestrator
from pipeline.job_store import JobStore
from pipeline.topic_pipeline import create_topic_package

app=FastAPI(title="Kids Content Engine",version="2.0.0")
ROOT=Path(os.getenv("WORK_ROOT","/tmp/kids-content-engine")); ROOT.mkdir(parents=True,exist_ok=True)
STORE=JobStore(str(ROOT))

class RenderJob(BaseModel):
    episode:str | None=None
    topic:str | None=None
    duration:float=30
    publish:bool=False
    dry_run:bool=True

def safe_episode(path:str):
    p=Path(path)
    if p.is_absolute() or ".." in p.parts: raise HTTPException(400,"invalid episode path")
    candidate=(Path.cwd()/p).resolve()
    if not candidate.is_file(): raise HTTPException(404,"episode not found")
    return str(candidate)

@app.get("/health")
def health():
    return {"status":"ok","service":"kids-content-engine","version":"2.0.0","render_enabled":os.getenv("RENDER_ENABLED","0")}

@app.get("/")
def root():
    return {"service":"kids-content-engine","status":"ready","version":"2.0.0"}

def process_job(job_id, job):
    try:
        STORE.update(job_id, status="processing")
        episode=job.episode
        if job.topic:
            episode=create_topic_package(job.topic,ROOT,duration=job.duration)["episode"]
        else:
            episode=safe_episode(episode)
        result=Orchestrator(str(ROOT)).run(episode,publish=job.publish,dry_run=job.dry_run)
        STORE.update(job_id,status="completed",result=result)
    except Exception as exc:
        STORE.update(job_id,status="failed",error=str(exc))

@app.post("/jobs")
def create_job(job:RenderJob, background_tasks: BackgroundTasks):
    if not job.episode and not job.topic:
        raise HTTPException(400,"provide episode or topic")
    data=STORE.create(job.model_dump())
    background_tasks.add_task(process_job, data["id"], job)
    return {"status":"accepted","job_id":data["id"]}

@app.get("/jobs/{job_id}")
def get_job(job_id:str):
    data=STORE.get(job_id)
    if not data: raise HTTPException(404,"job not found")
    return data

@app.post("/run")
def run_job(job:RenderJob):
    if job.topic:
        episode=create_topic_package(job.topic,ROOT,duration=job.duration)["episode"]
    elif job.episode:
        episode=safe_episode(job.episode)
    else:
        raise HTTPException(400,"provide episode or topic")
    if job.publish and os.getenv("PUBLISH_ENABLED","0")!="1":
        raise HTTPException(403,"publishing disabled")
    try:
        return {"status":"completed","result":Orchestrator(str(ROOT)).run(
            episode,publish=job.publish,dry_run=job.dry_run)}
    except Exception as exc:
        raise HTTPException(500,str(exc))
