from pathlib import Path
import json
import shutil
import subprocess

def validate_render(path):
    p=Path(path)
    if not p.exists():
        return {"ok":False,"error":"file_not_found"}
    if p.stat().st_size < 1024:
        return {"ok":False,"error":"file_too_small","size":p.stat().st_size}
    ffprobe=shutil.which("ffprobe")
    if not ffprobe:
        return {"ok":True,"size":p.stat().st_size,"probe":"unavailable"}
    try:
        raw=subprocess.run([
            ffprobe,"-v","error","-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height",
            "-of","json",str(p)
        ],capture_output=True,text=True,check=True).stdout
        data=json.loads(raw)
        duration=float(data.get("format",{}).get("duration",0) or 0)
        streams=data.get("streams",[])
        has_video=any(s.get("codec_type")=="video" for s in streams)
        has_audio=any(s.get("codec_type")=="audio" for s in streams)
        if duration <= 0 or not has_video:
            return {"ok":False,"error":"invalid_video_stream","probe":data}
        return {
            "ok":True,"size":p.stat().st_size,"duration":duration,
            "has_video":has_video,"has_audio":has_audio,"probe":data
        }
    except (subprocess.CalledProcessError, ValueError, json.JSONDecodeError) as exc:
        return {"ok":False,"error":"ffprobe_failed","detail":str(exc)}
