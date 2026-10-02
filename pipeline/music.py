import subprocess
from pathlib import Path

def create_music_bed(duration, output, mood="happy"):
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    freq={"happy":523,"calm":392,"playful":659}.get(mood,523)
    subprocess.run(["ffmpeg","-y","-f","lavfi","-i",f"sine=frequency={freq}:duration={duration}",
                    "-af","volume=0.025","-c:a","aac","-b:a","96k",str(output)],check=True,capture_output=True)
    return str(output)
