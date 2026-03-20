---
name: topaz-video
description: AI-powered video processing CLI using Topaz Video AI - upscale, enhance, stabilize, and interpolate videos with neural networks
---

# Topaz Video CLI Skill

AI-powered video processing using Topaz Video AI models directly from your terminal.

## Capabilities

- **Video Upscaling**: Enhance resolution with AI (1x, 2x, 4x, 8x)
- **Quality Enhancement**: Denoise, sharpen, recover details
- **Video Stabilization**: Smooth shaky footage
- **Frame Interpolation**: Create smooth slow-motion

## Triggering

This skill activates when you mention:
- "video", "upscale", "enhance", "stabilize", "interpolate"
- "Topaz", "TVAI", "Topaz Video"
- "slow motion", "frame interpolation"

## Usage

```bash
# Basic upscale
topaz-video process input.mp4 output.mp4 --model enhance --ai-model iris-2 --scale 2

# With original bitrate
topaz-video process input.mp4 output.mp4 --model enhance --ai-model iris-2 --scale 2 --bitrate 2000k

# Video stabilization
topaz-video process input.mp4 output.mp4 --model stabilize --smoothness 8

# Slow motion
topaz-video process input.mp4 output.mp4 --model interpolate --slowmo 2 --fps 60
```

## AI Models

| Name | Best For |
|------|----------|
| iris-2 | General purpose, fast |
| artemis | Anime/cartoon |
| proteus | High quality |
| rhea | Speed priority |
| nyx | High-res sources |
| theia | Best quality |
| gfx | Screen recording |

## Parameters

- `--ai-model`: Model name (iris-2, artemis, proteus, etc.)
- `--scale`: Upscale factor (1, 2, 4, 8)
- `--noise`: Denoise strength (-1 to 1)
- `--details`: Detail recovery (-1 to 1)
- `--blur`: Sharpening (-1 to 1)
- `--bitrate`: Output video bitrate (e.g., 2000k, 5M)

## Requirements

- Topaz Video AI installed at `/Applications/Topaz Video.app`
- Python 3.9+

## Notes

- Use `--bitrate` to control output file size (default is very high quality ~50Mbps)
- For ~2Mbps output matching original quality: `--bitrate 2000k`
- First time using a model? Open Topaz Video GUI to download it
