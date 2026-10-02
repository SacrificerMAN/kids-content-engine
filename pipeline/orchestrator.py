import os
from pathlib import Path
from .render_manager import RenderManager
from .publisher import Publisher
from .quality_control import validate_render
from .metadata import build_metadata
from .schema import load_episode
from .thumbnail import create_thumbnail_svg
from .audio import make_audio
from .ffmpeg_pipeline import mux_audio
from .asset_manifest import build_asset_manifest
from .production_manifest import write_production_manifest

class Orchestrator:
    def __init__(self,root=None):
        self.root=Path(root or os.getenv('WORK_ROOT','/tmp/kids-content-engine'))
        self.rm=RenderManager(str(self.root))

    def run(self,episode_path,publish=False,dry_run=True):
        ep=load_episode(episode_path)
        prepared=self.rm.prepare(episode_path)
        metadata=build_metadata(ep)
        job=Path(prepared['job_dir'])
        thumb=create_thumbnail_svg(str(job/'thumbnail.svg'), ep.title)
        asset_manifest=build_asset_manifest(ep, job)
        render=self.rm.render(prepared,dry_run=dry_run)
        audio_path=job/'audio.m4a'
        final_path=job/'final.mp4'
        audio_status='not_generated'
        if dry_run:
            audio_status='dry_run'
        elif Path(render['output']).exists():
            narration=" ".join(ep.metadata.get("narration", [])) or f"Welcome to {ep.title}. Let's learn and have fun together."
            make_audio(narration,ep.duration,audio_path)
            mux_audio(render['output'],audio_path,final_path)
            render['output']=str(final_path)
            audio_status='generated'
        qc=validate_render(render['output']) if Path(render['output']).exists() else {'ok':dry_run,'status':'not_rendered'}
        result={
            'prepared':prepared,'metadata':metadata,'thumbnail':thumb,'asset_manifest':asset_manifest,
            'audio':{'status':audio_status,'path':str(audio_path)},
            'render':render,'qc':qc
        }
        production_manifest=write_production_manifest(job, title=metadata['title'], topic=ep.metadata.get('topic'), render=render, audio=audio_status, qc=qc, asset_manifest=asset_manifest)
        result['production_manifest']=production_manifest
        if publish:
            if not qc.get('ok',False):
                raise RuntimeError('publishing blocked because QC did not pass')
            result['publish']=[r.__dict__ for r in Publisher(dry_run=dry_run).publish(
                render['output'], metadata['title'], metadata['description'])]
        return result
