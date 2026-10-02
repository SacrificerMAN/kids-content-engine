import os
from pathlib import Path
from .render_manager import RenderManager
from .publisher import Publisher
from .quality_control import validate_render
from .metadata import build_metadata
from .schema import load_episode
from .thumbnail import create_thumbnail_svg

class Orchestrator:
    def __init__(self,root=None):
        self.root=Path(root or os.getenv('WORK_ROOT','/tmp/kids-content-engine'))
        self.rm=RenderManager(str(self.root))

    def run(self,episode_path,publish=False,dry_run=True):
        ep=load_episode(episode_path)
        prepared=self.rm.prepare(episode_path)
        metadata=build_metadata(ep)
        thumb=create_thumbnail_svg(str(Path(prepared['job_dir'])/'thumbnail.svg'), ep.title)
        render=self.rm.render(prepared,dry_run=dry_run)
        qc=validate_render(render['output']) if Path(render['output']).exists() else {'ok':dry_run,'status':'not_rendered'}
        result={'prepared':prepared,'metadata':metadata,'thumbnail':thumb,'render':render,'qc':qc}
        if publish:
            if not qc.get('ok',False):
                raise RuntimeError('publishing blocked because QC did not pass')
            result['publish']=[r.__dict__ for r in Publisher(dry_run=dry_run).publish(
                render['output'], metadata['title'], metadata['description'])]
        return result
