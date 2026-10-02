import subprocess
from pathlib import Path

def mix_voice_music(voice,music,output):
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-y","-i",str(voice),"-i",str(music),
                    "-filter_complex","[1:a]volume=0.18[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
                    "-map","[a]","-c:a","aac","-b:a","160k",str(output)],check=True)
    return str(output)
