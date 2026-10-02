# Kids Content Engine

Autonomous, original preschool 3D content production pipeline.

## Goal

Give the engine a topic such as "colors", "animals", or "alphabet". The pipeline creates an original preschool episode package, generates a procedural 3D scene, renders an MP4, creates audio, runs QC, generates metadata and a thumbnail, and exposes gated publishing adapters.

## Flow

Topic -> episode generator -> scene JSON -> procedural Blender scene -> animated MP4 -> local TTS/audio -> final MP4 -> QC -> metadata/thumbnail -> publishing adapters.

## Studio UI

The root URL serves a browser-based **Kids Content Studio** dashboard. It can submit topic jobs, choose preview vs real-render mode, inspect engine status, and monitor recent jobs.

## API

- GET `/health`
- GET `/` — Studio UI
- GET `/api` — API status
- GET `/jobs` — recent jobs
- POST `/jobs` with `{"topic":"colors","duration":30,"dry_run":true}`
- GET `/jobs/{job_id}`
- POST `/run` — synchronous execution endpoint

Jobs submitted through `/jobs` are accepted immediately and processed as FastAPI background tasks. For high-volume production, replace the in-process background task with a durable queue and dedicated Blender workers.

## Rendering

The normal Railway API image is intentionally lightweight. Heavy Blender rendering uses `Dockerfile.render`, which installs Blender, FFmpeg and espeak-ng. Set `RENDER_ENABLED=1` on a Blender-capable worker. The Blender script writes an animated H.264 MP4.

## Audio

The render worker uses espeak-ng when available and falls back to a quiet generated audio bed. This is an engineering fallback, not a studio-quality child voice. A production TTS provider can be added behind the same `make_audio` interface.

## Publishing

Publishing remains credential-gated. YouTube, Facebook and Instagram must not be treated as successful until their adapters are implemented and tested with real platform credentials. The current publisher layer deliberately reports disabled/not-implemented rather than pretending success.

## Safety and originality

The engine creates original characters and story concepts. It is not designed to reproduce another children's show's characters, branding, episodes, or distinctive assets.

## Configuration

`WORK_ROOT`, `RENDER_ENABLED`, `BLENDER_BIN`, `BLENDER_TIMEOUT_SEC`, `PUBLISH_ENABLED`, `YOUTUBE_ACCESS_TOKEN`, `FACEBOOK_ACCESS_TOKEN`, `INSTAGRAM_ACCESS_TOKEN`.

Never commit credentials.


## Production providers

### AI content
Set `OPENAI_API_KEY` to enable LLM-generated story structure, lyrics, narration and scene prompts. Without it, the engine uses a deterministic original fallback.

### Voice
Set `TTS_PROVIDER=elevenlabs`, `ELEVENLABS_API_KEY`, and `ELEVENLABS_VOICE_ID` for provider-based voice generation. The local worker continues to support espeak-ng as an engineering fallback.

### Audio
The production audio path now creates a voice track, a low-volume music bed, then mixes them before muxing into the rendered MP4.

### Publishing
YouTube publishing is implemented behind `PUBLISH_ENABLED=1` and `YOUTUBE_ACCESS_TOKEN`. Default privacy is `private`. Facebook/Instagram remain explicit adapter targets rather than simulated uploads.

### Artifacts
The local artifact interface is available now. For Railway-scale production, point `ARTIFACT_ROOT` at a mounted/persistent storage layer or replace the provider with object storage.

## Production roadmap
The architecture is ready for a durable external queue, dedicated GPU Blender workers, object storage, richer reusable 3D asset libraries, and additional social-platform adapters.
