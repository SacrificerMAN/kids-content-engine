import os
from pathlib import Path
from .render_manager import RenderManager
from .publisher import Publisher
from .quality_control import validate_render
class Orchestrator:
    def __init__(self,root=None): self.root=Path(root or os.getenv('WORK_ROOT','/tmp/kids-content-engine')); self.rm=RenderManager(str(self.root))
    def run(self,episode_path,publish=False,dry_run=True):
        prepared=self.rm.prepare(episode_path); render=self.rm.render(prepared,dry_run=dry_run)
        qc=validate_render(render['output']) if Path(render['output']).exists() else {'ok':dry_run,'status':'not_rendered'}
        result={'prepared':prepared,'render':render,'qc':qc}
        if publish: result['publish']=[r.__dict__ for r in Publisher(dry_run=dry_run).publish(render['output'],Path(episode_path).stem)]
        return result
