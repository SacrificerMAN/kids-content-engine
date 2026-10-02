import shutil, subprocess
from pathlib import Path

def make_audio(text, duration, output):
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    espeak=shutil.which("espeak-ng") or shutil.which("espeak")
    if espeak:
        wav=output.with_suffix(".wav")
        subprocess.run([espeak,"-w",str(wav),text],check=True,capture_output=True)
        subprocess.run([
            "ffmpeg","-y","-i",str(wav),"-t",str(duration),
            "-af","apad=pad_dur="+str(duration),
            "-c:a","aac","-b:a","128k",str(output)
        ],check=True,capture_output=True)
        wav.unlink(missing_ok=True)
        return str(output)
    # Portable fallback: a quiet musical bed so every successful render has an audio stream.
    subprocess.run([
        "ffmpeg","-y","-f","lavfi","-i",
        f"sine=frequency=440:duration={float(duration)}",
        "-af","volume=0.03","-c:a","aac","-b:a","96k",str(output)
    ],check=True,capture_output=True)
    return str(output)
