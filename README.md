# Kids Content Engine

Production-oriented orchestration for an original preschool 3D animation pipeline. It uses original characters/assets and does not reproduce another show's characters, branding, or episodes.

Flow: Episode JSON -> validation -> procedural Blender scene recipe -> optional Blender render -> FFmpeg hooks -> QC -> publishing adapters.

Railway runs the FastAPI orchestration API. Heavy Blender rendering is opt-in through RENDER_ENABLED=1 and should run on a Blender-capable worker. Default operation is safe dry-run mode.

Endpoints: GET /health, GET /, POST /jobs, POST /run.

Example POST /run body: {"episode":"content/demo_episode.json","publish":false,"dry_run":true}

Variables: WORK_ROOT, RENDER_ENABLED, BLENDER_BIN, BLENDER_TIMEOUT_SEC, PUBLISH_ENABLED, YOUTUBE_ACCESS_TOKEN, FACEBOOK_ACCESS_TOKEN, INSTAGRAM_ACCESS_TOKEN.

Credentials are environment variables only; never commit them.

GitHub Actions validates the project on pushes to main, on manual dispatch, and daily. Railway can automatically deploy new commits from the connected branch.

For real animation rendering, use a dedicated Blender-capable worker/GPU service and persistent object storage for MP4 artifacts. The API service should remain responsive and coordinate jobs rather than acting as a render farm.
