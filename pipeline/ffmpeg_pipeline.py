import shutil, subprocess, json
from pathlib import Path

def ffmpeg_available(): return shutil.which('ffmpeg') is not None

def mux_audio(video,audio,output):
    if not ffmpeg_available(): raise RuntimeError('ffmpeg is not installed')
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-y','-i',video,'-i',audio,'-map','0:v:0','-map','1:a:0','-c:v','copy','-shortest',output],check=True)
    return output

def probe(path):
    if not ffmpeg_available(): return {'available':False}
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size','-of','json',path],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)
