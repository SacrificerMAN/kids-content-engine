import os, sys
from .orchestrator import Orchestrator

if __name__=="__main__":
    episode=os.getenv("EPISODE","content/demo_episode.json")
    dry=os.getenv("RENDER_ENABLED","0")!="1"
    result=Orchestrator().run(episode,publish=False,dry_run=dry)
    print(result)
    if result.get("qc",{}).get("ok") is False: sys.exit(1)
