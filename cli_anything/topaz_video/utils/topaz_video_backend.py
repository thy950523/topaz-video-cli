"""Topaz Video backend - invokes bundled CLI tools.

This module provides access to the tools bundled within the Topaz Video app:
- ffmpeg (with Topaz AI filters)
- ffprobe (media analysis)
- iconvert (image conversion)
- oiiotool (image processing)
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional


# Default Topaz Video app location on macOS
DEFAULT_TOPAZ_VIDEO_APP = "/Applications/Topaz Video.app"


def get_model_dir() -> Path:
    """Get the Topaz Video models directory."""
    app_path = find_topaz_video_app()
    return app_path / "Contents" / "Resources" / "models"


def get_env() -> dict:
    """Get environment variables for Topaz Video tools."""
    env = os.environ.copy()
    model_dir = get_model_dir()
    env["TVAI_MODEL_DIR"] = str(model_dir)
    env["TVAI_MODEL_DATA_DIR"] = str(model_dir)
    return env


def find_topaz_video_app() -> Path:
    """Find the Topaz Video app location.

    Returns:
        Path to Topaz Video.app

    Raises:
        RuntimeError: If Topaz Video is not installed
    """
    app_path = Path(DEFAULT_TOPAZ_VIDEO_APP)
    if app_path.exists():
        return app_path
    raise RuntimeError(
        f"Topaz Video not found at {DEFAULT_TOPAZ_VIDEO_APP}\n"
        "Please install Topaz Video from https://topazlabs.com/video-ai/"
    )


def get_topaz_video_cli_path(tool_name: str) -> Path:
    """Get the path to a CLI tool bundled with Topaz Video.

    Args:
        tool_name: Name of the tool (ffmpeg, ffprobe, iconvert, oiiotool)

    Returns:
        Path to the tool executable

    Raises:
        RuntimeError: If the tool is not found
    """
    app_path = find_topaz_video_app()
    tool_path = app_path / "Contents" / "MacOS" / tool_name

    if tool_path.exists() and os.access(tool_path, os.X_OK):
        return tool_path

    # Fallback to system version if available
    system_path = shutil.which(tool_name)
    if system_path:
        return Path(system_path)

    raise RuntimeError(
        f"Tool '{tool_name}' not found in Topaz Video app or system PATH\n"
        f"Expected: {tool_path}"
    )


def get_ffmpeg_path() -> Path:
    """Get the ffmpeg path (with Topaz AI filters)."""
    return get_topaz_video_cli_path("ffmpeg")


def get_ffprobe_path() -> Path:
    """Get the ffprobe path."""
    return get_topaz_video_cli_path("ffprobe")


def get_iconvert_path() -> Path:
    """Get the iconvert path."""
    return get_topaz_video_cli_path("iconvert")


def get_oiiotool_path() -> Path:
    """Get the oiiotool path."""
    return get_topaz_video_cli_path("oiiotool")


def probe_video(video_path: str) -> dict:
    """Probe a video file and return its metadata.

    Args:
        video_path: Path to the video file

    Returns:
        Dictionary containing video metadata

    Raises:
        RuntimeError: If ffprobe fails
    """
    ffprobe = get_ffprobe_path()
    cmd = [
        str(ffprobe),
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            env=get_env()
        )
        import json
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to probe video: {e.stderr}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse ffprobe output: {e}")


def get_video_info(video_path: str) -> dict:
    """Get simplified video information.

    Args:
        video_path: Path to the video file

    Returns:
        Dictionary with basic video info (duration, resolution, codec, etc.)
    """
    probe_data = probe_video(video_path)

    info = {
        "file": video_path,
        "format": probe_data.get("format", {}).get("format_name", "unknown"),
        "duration": probe_data.get("format", {}).get("duration", "0"),
        "size": probe_data.get("format", {}).get("size", "0"),
        "bitrate": probe_data.get("format", {}).get("bit_rate", "0"),
    }

    # Find video and audio streams
    for stream in probe_data.get("streams", []):
        if stream.get("codec_type") == "video":
            info["video_codec"] = stream.get("codec_name", "unknown")
            info["width"] = stream.get("width", 0)
            info["height"] = stream.get("height", 0)
            info["fps"] = stream.get("r_frame_rate", "0/1")
        elif stream.get("codec_type") == "audio":
            info["audio_codec"] = stream.get("codec_name", "unknown")
            info["audio_channels"] = stream.get("channels", 0)
            info["audio_sample_rate"] = stream.get("sample_rate", "0")

    return info


# Process model types
class ProcessModel:
    UPSCALE = "upscale"
    ENHANCE = "enhance"
    STABILIZE = "stabilize"
    INTERPOLATE = "interpolate"


def _build_upscale_filter(
    ai_model: Optional[str] = None,
    scale: int = 2,
    # Model parameters
    preblur: Optional[float] = None,
    noise: Optional[float] = None,
    details: Optional[float] = None,
    halo: Optional[float] = None,
    blur: Optional[float] = None,
    compression: Optional[float] = None,
    prenoise: Optional[float] = None,
    grain: Optional[float] = None,
    gsize: Optional[float] = None,
    kcolor: Optional[int] = None,
    blend: Optional[float] = None,
    # Device parameters
    device: Optional[str] = None,
    vram: Optional[float] = None,
    instances: Optional[int] = None,
) -> str:
    """Build tvai_up filter string with parameters."""
    # Use specified AI model or default to ahq-12 (high quality)
    model_name = ai_model if ai_model else "ahq-12"
    params = [f"model={model_name}", f"scale={scale}", "download=1"]

    if device is not None:
        params.append(f"device={device}")
    if vram is not None:
        params.append(f"vram={vram}")
    if instances is not None:
        params.append(f"instances={instances}")

    # Quality parameters
    if preblur is not None:
        params.append(f"preblur={preblur}")
    if noise is not None:
        params.append(f"noise={noise}")
    if details is not None:
        params.append(f"details={details}")
    if halo is not None:
        params.append(f"halo={halo}")
    if blur is not None:
        params.append(f"blur={blur}")
    if compression is not None:
        params.append(f"compression={compression}")
    if prenoise is not None:
        params.append(f"prenoise={prenoise}")
    if grain is not None:
        params.append(f"grain={grain}")
    if gsize is not None:
        params.append(f"gsize={gsize}")
    if kcolor is not None:
        params.append(f"kcolor={kcolor}")
    if blend is not None:
        params.append(f"blend={blend}")

    return "tvai_up=" + ":".join(params)


def _build_interpolate_filter(
    model: str = "interpolate",
    fps: Optional[float] = None,
    slowmo: Optional[float] = None,
    rdt: Optional[float] = None,
    # Device parameters
    device: Optional[str] = None,
    vram: Optional[float] = None,
    instances: Optional[int] = None,
) -> str:
    """Build tvai_fi (frame interpolation) filter string."""
    params = [f"model={model}"]

    if device is not None:
        params.append(f"device={device}")
    if vram is not None:
        params.append(f"vram={vram}")
    if instances is not None:
        params.append(f"instances={instances}")
    if fps is not None:
        params.append(f"fps={fps}")
    if slowmo is not None:
        params.append(f"slowmo={slowmo}")
    if rdt is not None:
        params.append(f"rdt={rdt}")

    return "tvai_fi=" + ":".join(params)


def _build_stabilize_filter(
    model: str = "stabilize",
    # Stabilization parameters
    smoothness: Optional[float] = None,
    full: Optional[bool] = None,
    ws: Optional[int] = None,
    csx: Optional[float] = None,
    csy: Optional[float] = None,
    dof: Optional[int] = None,
    roll: Optional[bool] = None,
    reduce: Optional[int] = None,
    # Device parameters
    device: Optional[str] = None,
    vram: Optional[float] = None,
    instances: Optional[int] = None,
) -> str:
    """Build tvai_stb (stabilization) filter string."""
    params = [f"model={model}"]

    if device is not None:
        params.append(f"device={device}")
    if vram is not None:
        params.append(f"vram={vram}")
    if instances is not None:
        params.append(f"instances={instances}")

    # Stabilization parameters
    if smoothness is not None:
        params.append(f"smoothness={smoothness}")
    if full is not None:
        params.append(f"full={1 if full else 0}")
    if ws is not None:
        params.append(f"ws={ws}")
    if csx is not None:
        params.append(f"csx={csx}")
    if csy is not None:
        params.append(f"csy={csy}")
    if dof is not None:
        params.append(f"dof={dof}")
    if roll is not None:
        params.append(f"roll={1 if roll else 0}")
    if reduce is not None:
        params.append(f"reduce={reduce}")

    return "tvai_stb=" + ":".join(params)


def process_video(
    input_path: str,
    output_path: str,
    model: str = "upscale",
    ai_model: Optional[str] = None,
    scale: int = 2,
    # Upscale/Enhance parameters
    preblur: Optional[float] = None,
    noise: Optional[float] = None,
    details: Optional[float] = None,
    halo: Optional[float] = None,
    blur: Optional[float] = None,
    compression: Optional[float] = None,
    prenoise: Optional[float] = None,
    grain: Optional[float] = None,
    gsize: Optional[float] = None,
    kcolor: Optional[int] = None,
    blend: Optional[float] = None,
    # Interpolate parameters
    fps: Optional[float] = None,
    slowmo: Optional[float] = None,
    rdt: Optional[float] = None,
    # Stabilize parameters
    smoothness: Optional[float] = None,
    stabilize_full: Optional[bool] = None,
    ws: Optional[int] = None,
    csx: Optional[float] = None,
    csy: Optional[float] = None,
    dof: Optional[int] = None,
    roll: Optional[bool] = None,
    reduce: Optional[int] = None,
    # Device parameters
    device: Optional[str] = None,
    vram: Optional[float] = None,
    instances: Optional[int] = None,
    # Output parameters
    codec: str = "h264_videotoolbox",
    preset: str = "medium",
    crf: int = 23,
    qv: int = 82,  # Quantization value for VideoToolbox (1-1024, higher = lower quality)
    bitrate: Optional[str] = None,  # Video bitrate (e.g., "5M")
    audio_bitrate: str = "128k",
    extra_args: Optional[list] = None,
    show_progress: bool = True
) -> dict:
    """Process a video using Topaz AI filters via ffmpeg.

    Args:
        input_path: Path to input video
        output_path: Path to output video
        model: AI model to use (upscale, enhance, stabilize, interpolate)
        scale: Upscale factor (1, 2, 4, 8)

        # Upscale/Enhance parameters (for upscale/enhance models)
        preblur: Antialiasing/deblurring strength (-1 to 1)
        noise: ISO noise removal (-1 to 1)
        details: Texture recovery (-1 to 1)
        halo: Halo artifact removal (-1 to 1)
        blur: Additional sharpening (-1 to 1)
        compression: Codec artifact reduction (-1 to 1)
        prenoise: Noise to add before processing (0 to 0.1)
        grain: Grain to add to output (0 to 1)
        gsize: Grain size (0 to 5)
        kcolor: Color correction (0 or 1)
        blend: Input/output blend (0 to 1)

        # Frame interpolation parameters
        fps: Output frame rate
        slowmo: Slow motion factor (0.1 to 16)
        rdt: Replace duplicate threshold

        # Stabilization parameters
        smoothness: Amount of smoothness (0 to 16)
        stabilize_full: Full-frame stabilization (default True)
        ws: Window size for full-frame synthesis (0 to 512)
        csx: Canvas scale X (1 to 8)
        csy: Canvas scale Y (1 to 8)
        dof: Degrees of freedom (0-1111, each digit: rotation, h-pan, v-pan, scale)
        roll: Rolling shutter correction (0 or 1)
        reduce: Reduce motion jitters (0 to 5)

        # Device parameters
        device: Device to use (auto, cpu, gpu0, etc.)
        vram: Max memory usage (0.1 to 1)
        instances: Number of model instances (0 to 3)

        # Output parameters
        codec: Video codec (libx264, libx265, prores_ks, etc.)
        preset: Encoding preset (ultrafast to veryslow)
        crf: Constant Rate Factor (0-51, lower = better quality)
        audio_bitrate: Audio bitrate
        extra_args: Additional ffmpeg arguments
        show_progress: Whether to show progress

    Returns:
        Dictionary with processing result info
    """
    ffmpeg = get_ffmpeg_path()

    # Build the filter chain based on model
    filter_chain = []

    if model == "enhance":
        # Enhance = upscale + sharpen
        filter_chain.append(_build_upscale_filter(
            ai_model=ai_model,
            scale=scale,
            preblur=preblur,
            noise=noise,
            details=details,
            halo=halo,
            blur=blur if blur else 0.3,  # Add some sharpening for enhance
            compression=compression,
            prenoise=prenoise,
            grain=grain,
            gsize=gsize,
            kcolor=kcolor,
            blend=blend,
            device=device,
            vram=vram,
            instances=instances,
        ))
    elif model == "upscale":
        filter_chain.append(_build_upscale_filter(
            ai_model=ai_model,
            scale=scale,
            preblur=preblur,
            noise=noise,
            details=details,
            halo=halo,
            blur=blur,
            compression=compression,
            prenoise=prenoise,
            grain=grain,
            gsize=gsize,
            kcolor=kcolor,
            blend=blend,
            device=device,
            vram=vram,
            instances=instances,
        ))
    elif model == "stabilize":
        filter_chain.append(_build_stabilize_filter(
            model="stabilize",
            smoothness=smoothness,
            full=stabilize_full,
            ws=ws,
            csx=csx,
            csy=csy,
            dof=dof,
            roll=roll,
            reduce=reduce,
            device=device,
            vram=vram,
            instances=instances,
        ))
    elif model == "interpolate":
        filter_chain.append(_build_interpolate_filter(
            model="interpolate",
            fps=fps,
            slowmo=slowmo,
            rdt=rdt,
            device=device,
            vram=vram,
            instances=instances,
        ))
    else:
        raise ValueError(f"Unknown model: {model}. Use: upscale, enhance, stabilize, interpolate")

    filter_desc = ",".join(filter_chain)

    cmd = [
        str(ffmpeg),
        "-i", input_path,
        "-vf", filter_desc,
        "-c:v", codec,
    ]

    if codec in ("libx264", "libx265"):
        cmd.extend(["-crf", str(crf)])
    elif codec == "h264_videotoolbox":
        # Use bitrate if specified, otherwise use q:v
        if bitrate:
            cmd.extend(["-b:v", bitrate])
        else:
            # Use q:v for VideoToolbox (higher = lower quality, 1-1024)
            cmd.extend(["-b:v", "0", "-q:v", str(qv)])

    cmd.extend(["-c:a", "aac", "-b:a", audio_bitrate])

    if extra_args:
        cmd.extend(extra_args)

    cmd.append("-y")  # Overwrite output
    cmd.append(output_path)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            env=get_env()
        )

        # Get output file size
        output_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0

        return {
            "success": True,
            "input": input_path,
            "output": output_path,
            "model": model,
            "scale": scale,
            "output_size": output_size,
            "stderr": result.stderr if show_progress else ""
        }
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Video processing failed: {e.stderr}")


def convert_video(
    input_path: str,
    output_path: str,
    codec: str = "h264_videotoolbox",
    bitrate: Optional[str] = None,
    extra_args: Optional[list] = None
) -> dict:
    """Convert video to a different format/codec.

    Args:
        input_path: Path to input video
        output_path: Path to output video
        codec: Video codec (libx264, libx265, prores, etc.)
        bitrate: Video bitrate (e.g., "5M")
        extra_args: Additional ffmpeg arguments

    Returns:
        Dictionary with conversion result
    """
    ffmpeg = get_ffmpeg_path()

    cmd = [
        str(ffmpeg),
        "-i", input_path,
        "-c:v", codec,
    ]

    if bitrate:
        cmd.extend(["-b:v", bitrate])

    if codec == "prores_ks":
        cmd.extend(["-profile:v", "3"])  # ProRes 422 HQ

    cmd.extend(["-c:a", "aac", "-b:a", "128k"])

    if extra_args:
        cmd.extend(extra_args)

    cmd.append("-y")
    cmd.append(output_path)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            env=get_env()
        )

        output_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0

        return {
            "success": True,
            "input": input_path,
            "output": output_path,
            "codec": codec,
            "output_size": output_size,
        }
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Video conversion failed: {e.stderr}")
