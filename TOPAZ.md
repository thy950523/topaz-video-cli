# Topaz Video Analysis

## Software Overview

**Name:** Topaz Video AI
**Version:** 1.1.1
**Type:** macOS GUI Application
**Location:** `/Applications/Topaz Video.app`

## Architecture Analysis

### Bundled CLI Tools

The app bundles several CLI tools in `Contents/MacOS/`:

1. **ffmpeg** - Custom build with Topaz AI filters enabled (`--enable-tvai`)
   - Version: 2a8316c70 (FFmpeg with Topaz enhancements)
   - Used for video encoding/decoding with AI filters

2. **ffprobe** - Media analysis tool
   - Used for probing video metadata, streams, format info

3. **iconvert** - OpenImageIO image converter
   - Used for image format conversion
   - Version: OpenImageIO 3.0.4.0

4. **oiiotool** - OpenImageIO image processing tool
   - Advanced image manipulation

5. **Topaz Video** (main executable)
   - GUI application requiring display
   - Cannot run headlessly
   - Uses the bundled CLI tools internally

### Backend Engine

The core backend is **ffmpeg with Topaz's custom TVAI filters**. This is a modified ffmpeg build that includes:
- Video enhancement filters
- Upscaling models
- Stabilization
- Frame interpolation

### Data Model

- **Input:** Video files (MP4, MOV, AVI, MKV, etc.)
- **Output:** Processed video files
- **Processing models:** Topaz AI models stored in app's frameworks

## CLI Interface Strategy

Since Topaz Video is a GUI app without a native headless CLI, the CLI harness will:

1. **Use bundled ffmpeg** - The custom ffmpeg with `--enable-tvai` can be invoked directly
2. **Wrap ffmpeg commands** - Expose high-level operations like enhance, upscale, stabilize
3. **Filter mapping** - Map Topaz AI filter names to ffmpeg filter chains

### Available Operations (via ffmpeg)

Based on Topaz Video AI capabilities:
- `tvai_up` - Upscale video (2x, 4x, 8x)
- `tvai_enhance` - Enhance video quality
- `tvai_stabilize` - Video stabilization
- `tvai_interpolate` - Frame interpolation (slow-mo)

### Video Format Support

- **Input:** Most common video formats (ffmpeg supports)
- **Output:** MP4 (H.264/H.265), ProRes, etc.

## Command Groups

1. **project** - Project management (job queue, settings)
2. **process** - Video processing (enhance, upscale, stabilize)
3. **probe** - Media information and analysis
4. **convert** - Format conversion

## Implementation Notes

- The CLI must find the bundled tools relative to the app
- Fall back to system ffmpeg if bundled not available
- Use subprocess to invoke ffmpeg with Topaz filters
- Verify output files after processing
