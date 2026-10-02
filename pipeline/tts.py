import os, base64, subprocess, shutil
from pathlib import Path
import requests

def _local_tts(text, output):
    espeak=shutil.which("espeak-ng") or shutil.which("espeak")
    if not espeak: raise RuntimeError("No local TTS engine installed")
    wav=Path(output).with_suffix(".wav")
    subprocess.run([espeak,"-w",str(wav),text],check=True,capture_output=True)
    return str(wav)

def synthesize(text, output):
    provider=os.getenv("TTS_PROVIDER","local").lower()
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    if provider=="elevenlabs":
        key=os.getenv("ELEVENLABS_API_KEY")
        voice=os.getenv("ELEVENLABS_VOICE_ID")
        if not key or not voice: raise RuntimeError("ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID are required")
        url=f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
        r=requests.post(url,headers={"xi-api-key":key,"accept":"audio/mpeg","content-type":"application/json"},
                        json={"text":text,"model_id":os.getenv("ELEVENLABS_MODEL","eleven_multilingual_v2")},timeout=120)
        r.raise_for_status(); output.write_bytes(r.content); return str(output)
    if provider=="http":
        endpoint=os.getenv("TTS_ENDPOINT"); key=os.getenv("TTS_API_KEY","")
        if not endpoint: raise RuntimeError("TTS_ENDPOINT is required")
        r=requests.post(endpoint,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},
                        json={"text":text},timeout=120); r.raise_for_status()
        if r.headers.get("content-type","").startswith("audio/"):
            output.write_bytes(r.content)
        else:
            output.write_bytes(base64.b64decode(r.json()["audio"]))
        return str(output)
    return _local_tts(text, output)

def render_voice_track(text, duration, output):
    raw=Path(output).with_suffix(".source")
    synthesize(text,raw)
    subprocess.run(["ffmpeg","-y","-i",str(raw),"-t",str(duration),"-af",f"apad=pad_dur={duration}",
                    "-c:a","aac","-b:a","160k",str(output)],check=True,capture_output=True)
    raw.unlink(missing_ok=True)
    return str(output)
