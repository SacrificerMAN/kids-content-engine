# Kids Content Engine

Automated original preschool 3D animation pipeline.

## Flow
Episode JSON -> Blender procedural scenes -> FFmpeg -> QC -> publishing adapters.

The project is designed for original characters and assets, not reproduction of any existing show's characters or branding.

## Components
- Blender Python procedural scene generation
- Railway HTTP worker
- GitHub Actions orchestration
- FFmpeg assembly
- automated QC
- YouTube/Facebook/Instagram publishing adapters

Secrets are supplied through environment variables; never commit credentials.