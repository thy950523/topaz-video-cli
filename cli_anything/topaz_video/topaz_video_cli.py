"""Topaz Video CLI - Main entry point.

A command-line interface for Topaz Video AI processing.
"""

import click
import json
import os
import sys
from pathlib import Path

from cli_anything.topaz_video.utils.repl_skin import ReplSkin
from cli_anything.topaz_video.utils import topaz_video_backend
from cli_anything.topaz_video.core import project as project_module


@click.group(invoke_without_command=True)
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
@click.pass_context
def cli(ctx, json_output):
    """Topaz Video CLI - AI-powered video processing."""
    ctx.ensure_object(dict)
    ctx.obj["json_output"] = json_output

    # If no subcommand is given, enter REPL
    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


@cli.command()
def repl():
    """Start interactive REPL mode."""
    skin = ReplSkin("topaz_video", version="1.0.0")
    skin.print_banner()

    session = topaz_video_backend.Session()

    commands = {
        "help": "Show available commands",
        "probe <file>": "Probe video file metadata",
        "process <input> <output> [options]": "Process video with AI",
        "convert <input> <output> [options]": "Convert video format",
        "info": "Show Topaz Video info",
        "quit": "Exit the REPL",
    }
    skin.help(commands)

    skin.info("Enter commands or use --help for options")

    while True:
        try:
            user_input = input(skin.prompt()).strip()
        except (EOFError, KeyboardInterrupt):
            skin.print_goodbye()
            break

        if not user_input:
            continue

        parts = user_input.split()
        cmd = parts[0].lower()

        if cmd == "quit" or cmd == "exit":
            skin.print_goodbye()
            break
        elif cmd == "help":
            skin.help(commands)
        elif cmd == "info":
            _show_info(skin)
        elif cmd == "probe" and len(parts) >= 2:
            _cmd_probe(skin, parts[1])
        elif cmd == "process" and len(parts) >= 3:
            _cmd_process(skin, parts[1], parts[2], parts[3:])
        elif cmd == "convert" and len(parts) >= 3:
            _cmd_convert(skin, parts[1], parts[2], parts[3:])
        else:
            skin.error(f"Unknown command: {user_input}")
            skin.hint("Type 'help' for available commands")


def _show_info(skin):
    """Show Topaz Video info."""
    try:
        app_path = topaz_video_backend.find_topaz_video_app()
        ffmpeg_path = topaz_video_backend.get_ffmpeg_path()
        ffprobe_path = topaz_video_backend.get_ffprobe_path()

        skin.section("Topaz Video")
        skin.status("App Location", str(app_path))
        skin.status("FFmpeg", str(ffmpeg_path))
        skin.status("FFprobe", str(ffprobe_path))

        # Get ffmpeg version
        import subprocess
        result = subprocess.run(
            [str(ffmpeg_path), "-version"],
            capture_output=True,
            text=True
        )
        version_line = result.stdout.split("\n")[0]
        skin.status("Version", version_line)

        skin.success("Topaz Video CLI ready")
    except Exception as e:
        skin.error(str(e))


def _cmd_probe(skin, video_path: str):
    """Probe a video file."""
    if not os.path.exists(video_path):
        skin.error(f"File not found: {video_path}")
        return

    try:
        info = topaz_video_backend.get_video_info(video_path)

        skin.section(f"Video Info: {Path(video_path).name}")
        skin.status("Format", info.get("format", "unknown"))
        skin.status("Duration", f"{info.get('duration', '0')}s")
        skin.status("Size", f"{info.get('size', '0')} bytes")

        if "video_codec" in info:
            skin.status("Video Codec", info["video_codec"])
            skin.status("Resolution", f"{info['width']}x{info['height']}")
            skin.status("FPS", info.get("fps", "unknown"))

        if "audio_codec" in info:
            skin.status("Audio Codec", info["audio_codec"])
            skin.status("Audio Channels", str(info.get("audio_channels", 0)))

        skin.success("Probe complete")
    except Exception as e:
        skin.error(f"Probe failed: {e}")


def _cmd_process(skin, input_path: str, output_path: str, args: list):
    """Process a video with AI."""
    if not os.path.exists(input_path):
        skin.error(f"Input file not found: {input_path}")
        return

    # Parse options
    model = "enhance"
    scale = 2

    i = 0
    while i < len(args):
        if args[i] == "--model" and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        elif args[i] == "--scale" and i + 1 < len(args):
            scale = int(args[i + 1])
            i += 2
        else:
            i += 1

    skin.info(f"Processing: {input_path} -> {output_path}")
    skin.info(f"Model: {model}, Scale: {scale}")

    try:
        result = topaz_video_backend.process_video(
            input_path=input_path,
            output_path=output_path,
            model=model,
            scale=scale
        )

        skin.success(f"Processed: {output_path}")
        skin.status("Output Size", f"{result['output_size']:,} bytes")
    except Exception as e:
        skin.error(f"Processing failed: {e}")


def _cmd_convert(skin, input_path: str, output_path: str, args: list):
    """Convert video format."""
    if not os.path.exists(input_path):
        skin.error(f"Input file not found: {input_path}")
        return

    codec = "libx264"
    bitrate = None

    i = 0
    while i < len(args):
        if args[i] == "--codec" and i + 1 < len(args):
            codec = args[i + 1]
            i += 2
        elif args[i] == "--bitrate" and i + 1 < len(args):
            bitrate = args[i + 1]
            i += 2
        else:
            i += 1

    skin.info(f"Converting: {input_path} -> {output_path}")
    skin.info(f"Codec: {codec}, Bitrate: {bitrate or 'default'}")

    try:
        result = topaz_video_backend.convert_video(
            input_path=input_path,
            output_path=output_path,
            codec=codec,
            bitrate=bitrate
        )

        skin.success(f"Converted: {output_path}")
        skin.status("Output Size", f"{result['output_size']:,} bytes")
    except Exception as e:
        skin.error(f"Conversion failed: {e}")


# ── CLI Commands ─────────────────────────────────────────────────────


@cli.command()
@click.argument("video_path")
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
def probe(video_path, json_output):
    """Probe video file metadata."""
    if not os.path.exists(video_path):
        if json_output:
            print(json.dumps({"error": f"File not found: {video_path}"}))
        else:
            click.echo(f"Error: File not found: {video_path}", err=True)
        sys.exit(1)

    try:
        info = topaz_video_backend.get_video_info(video_path)
        if json_output:
            print(json.dumps(info, indent=2))
        else:
            click.echo(f"Video: {video_path}")
            click.echo(f"Format: {info.get('format', 'unknown')}")
            click.echo(f"Duration: {info.get('duration', '0')}s")
            if "video_codec" in info:
                click.echo(f"Resolution: {info['width']}x{info['height']}")
                click.echo(f"Video Codec: {info['video_codec']}")
                click.echo(f"FPS: {info.get('fps', 'unknown')}")
            if "audio_codec" in info:
                click.echo(f"Audio Codec: {info['audio_codec']}")
    except Exception as e:
        if json_output:
            print(json.dumps({"error": str(e)}))
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# Model options group
model_options = click.group()


# Main process command with all parameters
@cli.command()
@click.argument("input_path")
@click.argument("output_path")
@click.option("--model", "model", default="upscale",
              type=click.Choice(["upscale", "enhance", "stabilize", "interpolate"]),
              help="Processing mode")
@click.option("--ai-model", "ai_model",
              help="AI model name (e.g., ahq-12, gfx, etc.) - specifies which model to use")
@click.option("--scale", default=2, type=int, help="Upscale factor (1, 2, 4, 8)")

# Output options
@click.option("--codec", default="h264_videotoolbox", help="Output video codec (h264_videotoolbox, hevc_videotoolbox, prores_videotoolbox)")
@click.option("--preset", default="medium", help="Encoding preset (ultrafast to veryslow)")
@click.option("--crf", default=23, type=int, help="CRF quality (0-51, lower = better) - for libx264/libx265")
@click.option("--qv", default=82, type=int, help="Quantization value (1-1024, higher = lower quality) - for h264_videotoolbox")
@click.option("--bitrate", help="Video bitrate (e.g., 5M, 10M) - overrides qv")
@click.option("--audio-bitrate", default="128k", help="Audio bitrate")

# Device options
@click.option("--device", help="Device (auto, cpu, gpu0, etc.)")
@click.option("--vram", type=float, help="Max VRAM usage (0.1-1.0)")
@click.option("--instances", type=int, help="Number of model instances (0-3)")

# Upscale/Enhance quality parameters
@click.option("--preblur", type=float, help="Antialiasing/deblurring (-1 to 1)")
@click.option("--noise", type=float, help="ISO noise removal (-1 to 1)")
@click.option("--details", type=float, help="Texture recovery (-1 to 1)")
@click.option("--halo", type=float, help="Halo artifact removal (-1 to 1)")
@click.option("--blur", type=float, help="Additional sharpening (-1 to 1)")
@click.option("--compression", type=float, help="Codec artifact reduction (-1 to 1)")
@click.option("--prenoise", type=float, help="Noise to add before processing (0-0.1)")
@click.option("--grain", type=float, help="Grain to add to output (0-1)")
@click.option("--gsize", type=float, help="Grain size (0-5)")
@click.option("--kcolor/--no-kcolor", default=None, help="Color correction")
@click.option("--blend", type=float, help="Input/output blend (0-1)")

# Frame interpolation parameters
@click.option("--fps", type=float, help="Output frame rate")
@click.option("--slowmo", type=float, help="Slow motion factor (0.1-16)")
@click.option("--rdt", type=float, help="Replace duplicate threshold")

# Stabilization parameters
@click.option("--smoothness", type=float, help="Stabilization smoothness (0-16)")
@click.option("--stabilize-full/--no-stabilize-full", default=None, help="Full-frame stabilization")
@click.option("--ws", type=int, help="Window size (0-512)")
@click.option("--csx", type=float, help="Canvas scale X (1-8)")
@click.option("--csy", type=float, help="Canvas scale Y (1-8)")
@click.option("--dof", type=int, help="Degrees of freedom (0-1111)")
@click.option("--roll/--no-roll", default=None, help="Rolling shutter correction")
@click.option("--reduce", type=int, help="Reduce motion jitters (0-5)")

@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
def process(
    input_path, output_path,
    model, ai_model, scale,
    codec, preset, crf, qv, bitrate, audio_bitrate,
    device, vram, instances,
    preblur, noise, details, halo, blur, compression, prenoise, grain, gsize, kcolor, blend,
    fps, slowmo, rdt,
    smoothness, stabilize_full, ws, csx, csy, dof, roll, reduce,
    json_output
):
    """Process video with Topaz AI models.

    Models:
      - upscale: Upscale video (2x, 4x, 8x)
      - enhance: Upscale + sharpen for better quality
      - stabilize: Video stabilization
      - interpolate: Frame interpolation (slow-mo)

    Examples:
      # Basic upscale 2x with default AI model
      topaz-video process input.mp4 output.mp4 --model upscale --scale 2

      # Enhance with specific AI model
      topaz-video process input.mp4 output.mp4 --model enhance --ai-model ahq-12 --scale 4 --noise 0.2 --blur 0.3

      # Stabilize video
      topaz-video process input.mp4 output.mp4 --model stabilize --smoothness 8

      # Slow motion
      topaz-video process input.mp4 output.mp4 --model interpolate --slowmo 2 --fps 60
    """
    if not os.path.exists(input_path):
        if json_output:
            print(json.dumps({"error": f"Input file not found: {input_path}"}))
        else:
            click.echo(f"Error: Input file not found: {input_path}", err=True)
        sys.exit(1)

    try:
        if json_output:
            result = topaz_video_backend.process_video(
                input_path=input_path,
                output_path=output_path,
                model=model,
                ai_model=ai_model,
                scale=scale,
                # Output
                codec=codec,
                preset=preset,
                crf=crf,
                qv=qv,
                bitrate=bitrate,
                audio_bitrate=audio_bitrate,
                # Device
                device=device,
                vram=vram,
                instances=instances,
                # Upscale/Enhance
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
                # Interpolate
                fps=fps,
                slowmo=slowmo,
                rdt=rdt,
                # Stabilize
                smoothness=smoothness,
                stabilize_full=stabilize_full,
                ws=ws,
                csx=csx,
                csy=csy,
                dof=dof,
                roll=roll,
                reduce=reduce,
                show_progress=False
            )
            print(json.dumps(result, indent=2))
        else:
            click.echo(f"Processing: {input_path} -> {output_path}")
            click.echo(f"Model: {model}, Scale: {scale}x")

            result = topaz_video_backend.process_video(
                input_path=input_path,
                output_path=output_path,
                model=model,
                ai_model=ai_model,
                scale=scale,
                codec=codec,
                preset=preset,
                crf=crf,
                qv=qv,
                bitrate=bitrate,
                audio_bitrate=audio_bitrate,
                device=device,
                vram=vram,
                instances=instances,
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
                fps=fps,
                slowmo=slowmo,
                rdt=rdt,
                smoothness=smoothness,
                stabilize_full=stabilize_full,
                ws=ws,
                csx=csx,
                csy=csy,
                dof=dof,
                roll=roll,
                reduce=reduce,
            )

            click.echo(f"Success! Output: {output_path}")
            click.echo(f"Size: {result['output_size']:,} bytes")
    except Exception as e:
        if json_output:
            print(json.dumps({"error": str(e)}))
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("input_path")
@click.argument("output_path")
@click.option("--codec", default="libx264", help="Video codec (libx264, libx265, prores)")
@click.option("--bitrate", help="Video bitrate (e.g., 5M)")
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
def convert(input_path, output_path, codec, bitrate, json_output):
    """Convert video format."""
    if not os.path.exists(input_path):
        if json_output:
            print(json.dumps({"error": f"Input file not found: {input_path}"}))
        else:
            click.echo(f"Error: Input file not found: {input_path}", err=True)
        sys.exit(1)

    try:
        if json_output:
            result = topaz_video_backend.convert_video(
                input_path=input_path,
                output_path=output_path,
                codec=codec,
                bitrate=bitrate
            )
            print(json.dumps(result, indent=2))
        else:
            click.echo(f"Converting: {input_path} -> {output_path}")
            click.echo(f"Codec: {codec}, Bitrate: {bitrate or 'default'}")

            result = topaz_video_backend.convert_video(
                input_path=input_path,
                output_path=output_path,
                codec=codec,
                bitrate=bitrate
            )

            click.echo(f"Success! Output: {output_path}")
            click.echo(f"Size: {result['output_size']:,} bytes")
    except Exception as e:
        if json_output:
            print(json.dumps({"error": str(e)}))
        else:
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def info():
    """Show Topaz Video CLI information."""
    try:
        app_path = topaz_video_backend.find_topaz_video_app()
        ffmpeg_path = topaz_video_backend.get_ffmpeg_path()
        ffprobe_path = topaz_video_backend.get_ffprobe_path()

        click.echo("Topaz Video CLI")
        click.echo("=" * 40)
        click.echo(f"App Location: {app_path}")
        click.echo(f"FFmpeg: {ffmpeg_path}")
        click.echo(f"FFprobe: {ffprobe_path}")

        # Get ffmpeg version
        import subprocess
        result = subprocess.run(
            [str(ffmpeg_path), "-version"],
            capture_output=True,
            text=True
        )
        version_line = result.stdout.split("\n")[0]
        click.echo(f"Version: {version_line}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
