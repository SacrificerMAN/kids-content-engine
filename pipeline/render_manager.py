import os, json, shutil, subprocess
from pathlib import Path
from .schema import load_episode
from .blender_scene import write_blender_script

class RenderManager:
    def __init__(self, root):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)

    def prepare(self, episode_path):
        ep=load_episode(episode_path)
        job=self.root/safe_name(ep.title); job.mkdir(parents=True,exist_ok=True)
        (job/'manifest.json').write_text(json.dumps({
            'title':ep.title,'duration':ep.duration,'style':ep.style,
            'scenes':[s.__dict__ for s in ep.scenes],'characters':ep.characters,
            'metadata':ep.metadata
        },indent=2),encoding='utf-8')
        script=job/'scene.py'; write_blender_script(ep,script)
        return {'job_dir':str(job),'manifest':str(job/'manifest.json'),'blender_script':str(script)}

    def render(self, prepared, dry_run=True):
        out=Path(prepared['job_dir'])/'render.mp4'
        if dry_run or os.getenv('RENDER_ENABLED','0')!='1':
            return {'status':'prepared','dry_run':True,'output':str(out)}
        blender=shutil.which(os.getenv('BLENDER_BIN','blender')) or os.getenv('BLENDER_BIN','blender')
        p=subprocess.run([blender,'-b','--python',prepared['blender_script']],
                         capture_output=True,text=True,
                         timeout=int(os.getenv('BLENDER_TIMEOUT_SEC','3600')))
        if p.returncode:
            raise RuntimeError(p.stderr[-4000:] or p.stdout[-4000:])
        if not out.exists() or out.stat().st_size < 1024:
            raise RuntimeError('Blender completed without producing a valid render.mp4')
        return {'status':'rendered','dry_run':False,'output':str(out),'size':out.stat().st_size}

def safe_name(s):
    return ''.join(c.lower() if c.isalnum() else '_' for c in s).strip('_') or 'episode'
