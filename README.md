# Kids Content Engine

Autonomous, original preschool 3D content production pipeline.

## Goal

Give the engine a topic such as "colors", "animals", or "alphabet". The pipeline creates an original preschool episode package, generates a procedural 3D scene, renders an MP4, creates audio, runs QC, generates metadata and a thumbnail, and exposes gated publishing adapters.

## Flow

Topic -> episode generator -> scene JSON -> procedural Blender scene -> animated MP4 -> local TTS/audio -> final MP4 -> QC -> metadata/thumbnail -> publishing adapters.

## API

- GET `/health`
- GET `/`
- POST `/jobs` with `{"topic":"colors","duration":30,"dry_run":true}`
- GET `/jobs/{job_id}`
- POST `/run`

Jobs currently execute synchronously inside the API process. For high-volume production, move the same orchestrator behind a queue and dedicated Blender workers.

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
