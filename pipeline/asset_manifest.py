import json
from pathlib import Path

def build_asset_manifest(episode, job_dir):
    root=Path(job_dir)
    assets={
        "characters":[{"id":c,"type":"original_procedural_character","source":"blender_scene"} for c in episode.characters],
        "scenes":[
            {"index":i+1,"location":s.location,"actions":s.actions,"visual_prompt":getattr(s,"visual_prompt","")}
            for i,s in enumerate(episode.scenes)
        ],
        "audio":{"provider":"configured_tts_or_local_fallback"},
        "video":{"renderer":"blender","codec":"h264"},
        "thumbnail":{"source":"svg_template"}
    }
    path=root/"asset_manifest.json"
    path.write_text(json.dumps(assets,indent=2,ensure_ascii=False),encoding="utf-8")
    return str(path)
