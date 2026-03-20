# Topaz Video CLI

AI-powered video processing command-line interface using Topaz Video AI - supports upscaling, enhancement, stabilization, and frame interpolation.

[中文](./README-zh.md) | English

---

## Features

- 🎬 Video upscaling with AI models (Iris, Artemis, Proteus, etc.)
- 🔧 Customizable quality parameters (bitrate, quantization)
- 📦 Complete parameter mapping (GUI to CLI)
- ✅ 25+ test cases, 100% pass rate

---

## Quick Start

### 1. Install Dependencies

```bash
# Clone the project
git clone https://github.com/yourusername/topaz-video-cli.git
cd topaz-video-cli

# Install Python dependencies
pip install -e .
```

**Requirements:**
- Python 3.9+
- [Topaz Video AI](https://topazlabs.com/video-ai/) (must be installed at `/Applications/Topaz Video.app`)

### 2. Basic Usage

```bash
# View help
topaz-video --help

# Probe video info
topaz-video probe input.mp4

# 2x upscaling
topaz-video process input.mp4 output.mp4 --model enhance --scale 2 --ai-model iris-2
```

---

## Deployment Guide

### Claude Code Deployment

Claude Code is Anthropic's official CLI tool.

#### Option 1: Install from GitHub

```bash
# 1. Clone to Claude Code plugins directory
cd ~/.claude/plugins
git clone https://github.com/yourusername/topaz-video-cli.git topaz-video

# 2. Reload plugins
/reload-plugins

# 3. Verify installation
topaz-video --help
```

#### Option 2: Use plugin install command

```bash
# Install latest version
/plugin install topaz-video@github:yourusername/topaz-video-cli

# Install specific version
/plugin install topaz-video@github:yourusername/topaz-video-cli@v1.0.0
```

#### Option 3: Local Development

```bash
# 1. Clone project
git clone https://github.com/yourusername/topaz-video-cli.git
cd topaz-video-cli

# 2. Create symlink
mkdir -p ~/.claude/plugins
ln -s $(pwd) ~/.claude/plugins/topaz-video

# 3. Reload
/reload-plugins
```

#### Verify Claude Code Installation

```bash
# Test CLI
topaz-video info

# Should show:
# Topaz Video CLI
# App Location: /Applications/Topaz Video.app
# FFmpeg: /Applications/Topaz Video.app/Contents/MacOS/ffmpeg
```

---

### OpenClaw Deployment

OpenClaw is an open-source AI agent with similar skill system support.

#### Option 1: Project-level Installation (Recommended)

```bash
# 1. Clone project
git clone https://github.com/yourusername/topaz-video-cli.git

# 2. Copy skill to your project
cp -r topaz-video-cli/.openclaw/skills/topaz-video your-project/skills/

# 3. Clean up
rm -rf topaz-video-cli

# 4. Use in project
cd your-project
openclaw
```

#### Option 2: Global Installation

```bash
# 1. Clone project
git clone https://github.com/yourusername/topaz-video-cli.git

# 2. Create global skills directory
mkdir -p ~/.openclaw/skills

# 3. Copy skill
cp -r topaz-video-cli/.openclaw/skills/topaz-video ~/.openclaw/skills/

# 4. Clean up
rm -rf topaz-video-cli
```

#### Verify OpenClaw Installation

```bash
# Check status
openclaw status

# Should show topaz-video skill loaded
```

---

## Commands

### probe - Probe Video Information

```bash
topaz-video probe <video_path>
topaz-video probe video.mp4 --json
```

### process - Video Processing (Main Command)

```bash
topaz-video process <input> <output> [OPTIONS]
```

#### Model Options

| Flag | Description | Values |
|------|-------------|--------|
| `--model` | Processing mode | `upscale`, `enhance`, `stabilize`, `interpolate` |
| `--ai-model` | AI model name | See below |
| `--scale` | Upscale factor | 1, 2, 4, 8 |

#### AI Models

| GUI Name | CLI Name | Best For |
|----------|----------|----------|
| Iris | `iris-2` | General purpose, fast |
| Artemis | `artemis` | Anime/cartoon |
| Proteus | `proteus` | High quality |
| Rhea | `rhea` | Speed priority |
| Nyx | `nyx` | High-res sources |
| Theia | `theia` | Best quality |
| GFX | `gfx` | Screen recording |

#### Quality Parameters

| Flag | GUI Equivalent | Range |
|------|---------------|-------|
| `--noise` | Add noise | -1 to 1 |
| `--details` | Recover detail | -1 to 1 |
| `--blur` | Sharpen | -1 to 1 |
| `--preblur` | Anti-alias/deblur | -1 to 1 |
| `--halo` | Dehalo | -1 to 1 |
| `--compression` | Revert compression | -1 to 1 |
| `--grain` | Grain | 0 to 1 |

#### Output Quality Control

| Flag | Description | Example |
|------|-------------|---------|
| `--bitrate` | Video bitrate | `2000k`, `5M` |
| `--qv` | Quantization (1-1024) | Higher = lower quality |
| `--crf` | CRF quality (0-51) | Lower = better quality |
| `--codec` | Encoder | `h264_videotoolbox` |
| `--audio-bitrate` | Audio bitrate | `128k` |

### convert - Video Format Conversion

```bash
topaz-video convert input.mp4 output.mov --codec h264_videotoolbox
topaz-video convert input.mp4 output.mov --codec prores_videotoolbox
```

---

## Examples

### Example 1: 2x Upscale with Original Bitrate

```bash
# Probe original bitrate first
topaz-video probe input.mp4

# Process with original bitrate
topaz-video process input.mp4 output_2x.mp4 \
  --model enhance \
  --ai-model iris-2 \
  --scale 2 \
  --bitrate 2000k
```

### Example 2: Enhance Low Quality Video

```bash
topaz-video process input.mp4 output.mp4 \
  --model enhance \
  --ai-model proteus \
  --scale 2 \
  --noise 0.3 \
  --details 0.5
```

### Example 3: Video Stabilization

```bash
topaz-video process shaky.mp4 stable.mp4 \
  --model stabilize \
  --smoothness 8
```

### Example 4: Slow Motion

```bash
topaz-video process input.mp4 slowmo.mp4 \
  --model interpolate \
  --slowmo 2 \
  --fps 60
```

### Example 5: JSON Output (Programmatic)

```bash
topaz-video --json probe video.mp4
topaz-video --json process input.mp4 output.mp4 --model enhance --ai-model iris-2 --scale 2
```

---

## FAQ

### Q: Getting "Model not found" error?

**Solution**: First time using a model? Open Topaz Video GUI to download the model.

### Q: Output file too large?

**Solution**: Use `--bitrate` to control file size.
```bash
--bitrate 2000k   # ~2Mbps
--bitrate 5000k   # ~5Mbps
```

### Q: Where are the logs?

```
~/Library/Application Support/Topaz Labs LLC/Topaz Video/logs/
```

---

## Project Structure

```
topaz-video-cli/
├── .openclaw/                    # OpenClaw skill config
│   └── skills/
│       └── topaz-video/
│           └── SKILL.md
├── cli_anything/                 # Python package
│   └── topaz_video/
│       ├── topaz_video_cli.py   # CLI entry
│       ├── utils/
│       │   └── topaz_video_backend.py
│       └── tests/
├── SKILL.md                      # Claude Code skill definition
├── README.md                     # English docs
├── README-zh.md                  # Chinese docs
└── setup.py                      # Package config
```

---

## Development

### Run Tests

```bash
pytest cli_anything/topaz_video/tests/ -v
```

### Local Install

```bash
pip install -e .
topaz-video --help
```

---

## License

MIT License

---

## Links

- [Topaz Video AI](https://topazlabs.com/video-ai/)
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/overview)
- [OpenClaw GitHub](https://github.com/open-ai/OpenClaw)
