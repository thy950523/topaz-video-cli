---
name: cli-anything-topaz-video
description: CLI for Topaz Video AI - process videos with AI enhancement, upscaling, stabilization, and frame interpolation
---

# Topaz Video CLI

AI-powered video processing command-line interface using bundled Topaz Video tools.

## Installation

```bash
pip install cli-anything-topaz-video
```

Requires Topaz Video installed at `/Applications/Topaz Video.app`

## Commands

### probe
Probe video file metadata.

```bash
cli-anything-topaz-video probe <video_path>
cli-anything-topaz-video probe video.mp4 --json
```

### process
Process video with Topaz AI models.

```bash
# Basic upscale 2x
cli-anything-topaz-video process input.mp4 output.mp4 --model upscale --scale 2

# Enhance with specific AI model
cli-anything-topaz-video process input.mp4 output.mp4 --model enhance --ai-model ahq-12 --scale 4 --noise 0.2 --blur 0.3

# Stabilize video
cli-anything-topaz-video process input.mp4 output.mp4 --model stabilize --smoothness 8

# Frame interpolation (slow-mo)
cli-anything-topaz-video process input.mp4 output.mp4 --model interpolate --slowmo 2 --fps 60

# JSON output
cli-anything-topaz-video process input.mp4 output.mp4 --json
```

#### Model Options
- `--model` - Processing mode: upscale, enhance, stabilize, interpolate
- `--ai-model` - AI model name (e.g., ahq-12, gfx, etc.) - specifies which model to use
- `--scale` - Upscale factor: 1, 2, 4, 8

#### Quality Parameters (for upscale/enhance models)
- `--preblur` - Antialiasing/deblurring (-1 to 1)
- `--noise` - ISO noise removal (-1 to 1)
- `--details` - Texture recovery (-1 to 1)
- `--halo` - Halo artifact removal (-1 to 1)
- `--blur` - Additional sharpening (-1 to 1)
- `--compression` - Codec artifact reduction (-1 to 1)
- `--prenoise` - Noise to add before processing (0-0.1)
- `--grain` - Grain to add to output (0-1)
- `--gsize` - Grain size (0-5)
- `--kcolor/--no-kcolor` - Color correction
- `--blend` - Input/output blend (0-1)

#### Frame Interpolation Parameters
- `--fps` - Output frame rate
- `--slowmo` - Slow motion factor (0.1-16)
- `--rdt` - Replace duplicate threshold

#### Stabilization Parameters
- `--smoothness` - Stabilization smoothness (0-16)
- `--stabilize-full/--no-stabilize-full` - Full-frame stabilization
- `--ws` - Window size (0-512)
- `--csx` - Canvas scale X (1-8)
- `--csy` - Canvas scale Y (1-8)
- `--dof` - Degrees of freedom (0-1111)
- `--roll/--no-roll` - Rolling shutter correction
- `--reduce` - Reduce motion jitters (0-5)

#### Device Options
- `--device` - Device (auto, cpu, gpu0, etc.)
- `--vram` - Max VRAM usage (0.1-1.0)
- `--instances` - Number of model instances (0-3)

#### Output Options
- `--codec` - Video codec (libx264, libx265, prores_ks)
- `--preset` - Encoding preset (ultrafast to veryslow)
- `--crf` - CRF quality (0-51, lower = better)
- `--audio-bitrate` - Audio bitrate

### convert
Convert video format.

```bash
# Convert to H.264
cli-anything-topaz-video convert input.mp4 output.mov --codec libx264

# Convert to ProRes
cli-anything-topaz-video convert input.mp4 output.mov --codec prores_ks

# Convert with bitrate
cli-anything-topaz-video convert input.mp4 output.mp4 --bitrate 10M
```

### info
Show Topaz Video CLI and tool information.

```bash
cli-anything-topaz-video info
```

### repl
Start interactive REPL mode.

```bash
cli-anything-topaz-video
```

## Agent-Specific Notes

- Uses bundled ffmpeg/ffprobe from Topaz Video app
- All commands support `--json` for machine-readable output
- Error messages are clear and actionable
- Works with real video files for actual processing
- Supports comprehensive AI parameters for fine-tuned processing

## GUI to CLI Parameter Mapping

When using the GUI, here's how to map settings to CLI parameters:

### AI Model Names (from GUI to CLI)
| GUI Display Name | CLI --ai-model value |
|------------------|---------------------|
| Iris | iris-2 |
| Artemis | artemis |
| Proteus | proteus |
| Rhea | rhea |
| Nyx | nyx |
| Theia | theia |
| GFX | gfx |

### Complete Parameter Mapping (from log analysis)
Based on actual log file analysis:

| Log Parameter | GUI Setting | CLI Parameter | Example Value |
|---------------|-------------|---------------|---------------|
| model=iris-2 | AI Model: Iris | --ai-model iris-2 | iris-2 |
| scale=0 | Auto-detect scale | --scale | 2 |
| w=720, h=720 | Output: 720x720 | --scale 2 (auto) | 720x720 |
| preblur=0 | Anti-alias/deblur | --preblur | 0 |
| noise=0 | Reduce noise | --noise | 0 |
| details=0 | Recover detail | --details | 0 |
| halo=0 | Dehalo | --halo | 0 |
| blur=0 | Sharpen | --blur | 0 |
| compression=0 | Revert compression | --compression | 0 |
| device=-2 | Device: Auto | --device auto | -2 |
| vram=1 | VRAM: 100% | --vram | 1.0 |
| instances=1 | Instances: 1 | --instances | 1 |

### Example: Matching Your Screenshot
```bash
# Process with Iris model, 2x upscale to 720x720
# GUI settings: Iris, 720x720 (2x), noise=0, detail=0, grain=off
cli-anything-topaz-video process input.mp4 output.mp4 \
  --model enhance \
  --ai-model iris-2 \
  --scale 2 \
  --noise 0 \
  --details 0 \
  --grain 0
```

### Additional Parameters from Log
The log also reveals some additional parameters:
- `estimate=8` - Estimation mode (not exposed in CLI yet)
- `device=-2` - Auto device selection
- `vram=1` - Full VRAM usage
