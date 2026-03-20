# Topaz Video CLI

A command-line interface for Topaz Video AI video processing.

## Installation

### Prerequisites

1. **Topaz Video** must be installed at `/Applications/Topaz Video.app`
   - Download from: https://topazlabs.com/video-ai/

2. **Python 3.10+** is required

### Install the CLI

```bash
cd agent-harness
pip install -e .
```

## Usage

### Interactive REPL Mode

```bash
cli-anything-topaz-video
```

This starts an interactive shell with commands like:
- `probe <file>` - Show video metadata
- `process <input> <output>` - Process video with AI
- `convert <input> <output>` - Convert video format
- `info` - Show Topaz Video info

### One-Shot Commands

#### Probe Video

```bash
cli-anything-topaz-video probe /path/to/video.mp4
cli-anything-topaz-video probe /path/to/video.mp4 --json
```

#### Process Video with AI

```bash
# Enhance video quality
cli-anything-topaz-video process input.mp4 output.mp4 --model enhance

# Upscale video
cli-anything-topaz-video process input.mp4 output.mp4 --model upscale --scale 4

# Stabilize video
cli-anything-topaz-video process input.mp4 output.mp4 --model stabilize

# Interpolate frames (slow-mo)
cli-anything-topaz-video process input.mp4 output.mp4 --model interpolate
```

#### Convert Video Format

```bash
# Convert to H.264
cli-anything-topaz-video convert input.mp4 output.mov --codec libx264

# Convert to ProRes
cli-anything-topaz-video convert input.mp4 output.mov --codec prores_ks

# Convert with specific bitrate
cli-anything-topaz-video convert input.mp4 output.mp4 --bitrate 10M
```

#### Show Info

```bash
cli-anything-topaz-video info
```

## JSON Output

All commands support `--json` flag for machine-readable output:

```bash
cli-anything-topaz-video probe video.mp4 --json
cli-anything-topaz-video process input.mp4 output.mp4 --json
```

## Development

### Install for Development

```bash
pip install -e .
```

### Test

```bash
# Run unit tests
python -m pytest cli_anything/topaz_video/tests/test_core.py -v

# Run all tests with installed CLI
CLI_ANYTHING_FORCE_INSTALLED=1 python -m pytest cli_anything/topaz_video/tests/ -v
```

## Architecture

- `topaz_video_cli.py` - Main CLI entry point
- `core/project.py` - Project management
- `core/session.py` - Session management
- `utils/topaz_video_backend.py` - Backend wrapper for Topaz CLI tools
- `utils/repl_skin.py` - REPL interface styling
