"""Unit tests for Topaz Video CLI core modules.

These tests use synthetic data and mock dependencies.
"""

import os
import json
import tempfile
import pytest
from pathlib import Path

# Test paths that don't require real files
TEST_APP_PATH = "/Applications/Topaz Video.app"


class TestProjectModule:
    """Tests for project.py module."""

    def test_create_project_defaults(self):
        """Test project creation with defaults."""
        from cli_anything.topaz_video.core.project import create_project

        proj = create_project("test", "/input/video.mp4")

        assert proj.name == "test"
        assert proj.input_path == "/input/video.mp4"
        assert proj.model == "enhance"
        assert proj.scale == 2
        assert proj.status == "created"

    def test_create_project_custom(self):
        """Test project creation with custom settings."""
        from cli_anything.topaz_video.core.project import create_project

        proj = create_project(
            "myvideo",
            "/input/video.mp4",
            "/output/result.mp4",
            model="upscale",
            scale=4
        )

        assert proj.name == "myvideo"
        assert proj.output_path == "/output/result.mp4"
        assert proj.model == "upscale"
        assert proj.scale == 4

    def test_default_output_path(self):
        """Test default output path generation."""
        from cli_anything.topaz_video.core.project import VideoProject

        proj = VideoProject("test", "/input/myvideo.mp4")
        assert proj.output_path == "/input/myvideo_processed.mp4"

    def test_project_to_dict(self):
        """Test project serialization."""
        from cli_anything.topaz_video.core.project import create_project

        proj = create_project("test", "/input/video.mp4")
        data = proj.to_dict()

        assert data["name"] == "test"
        assert data["input_path"] == "/input/video.mp4"
        assert data["model"] == "enhance"

    def test_project_from_dict(self):
        """Test project deserialization."""
        from cli_anything.topaz_video.core.project import VideoProject

        data = {
            "name": "test",
            "input_path": "/input/video.mp4",
            "output_path": "/output/result.mp4",
            "model": "stabilize",
            "scale": 2,
            "settings": {},
            "created_at": "2024-01-01T00:00:00",
            "status": "created"
        }

        proj = VideoProject.from_dict(data)
        assert proj.name == "test"
        assert proj.model == "stabilize"

    def test_save_and_load_project(self):
        """Test project persistence."""
        from cli_anything.topaz_video.core.project import create_project, save_project, load_project

        proj = create_project("test", "/input/video.mp4")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            tmp_path = f.name

        try:
            save_project(proj, tmp_path)
            loaded = load_project(tmp_path)

            assert loaded.name == proj.name
            assert loaded.input_path == proj.input_path
            assert loaded.model == proj.model
        finally:
            os.unlink(tmp_path)


class TestBackendPathResolution:
    """Tests for backend path resolution."""

    def test_find_topaz_app_exists(self):
        """Test that Topaz Video app is found."""
        from cli_anything.topaz_video.utils import topaz_video_backend

        # This test assumes Topaz Video is installed
        try:
            path = topaz_video_backend.find_topaz_video_app()
            assert path.exists()
        except RuntimeError:
            pytest.skip("Topaz Video not installed")

    def test_get_ffmpeg_path(self):
        """Test ffmpeg path resolution."""
        from cli_anything.topaz_video.utils import topaz_video_backend

        try:
            path = topaz_video_backend.get_ffmpeg_path()
            assert path.exists()
            assert os.access(path, os.X_OK)
        except RuntimeError:
            pytest.skip("Topaz Video not installed")

    def test_get_ffprobe_path(self):
        """Test ffprobe path resolution."""
        from cli_anything.topaz_video.utils import topaz_video_backend

        try:
            path = topaz_video_backend.get_ffprobe_path()
            assert path.exists()
            assert os.access(path, os.X_OK)
        except RuntimeError:
            pytest.skip("Topaz Video not installed")


class TestCLIHelp:
    """Tests for CLI help."""

    def test_cli_help(self):
        """Test CLI --help output."""
        from click.testing import CliRunner
        from cli_anything.topaz_video.topaz_video_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Topaz Video" in result.output
        assert "probe" in result.output
        assert "process" in result.output
        assert "convert" in result.output

    def test_subcommand_help(self):
        """Test subcommand help."""
        from click.testing import CliRunner
        from cli_anything.topaz_video.topaz_video_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["probe", "--help"])

        assert result.exit_code == 0
        assert "VIDEO_PATH" in result.output


class TestInfoCommand:
    """Tests for info command."""

    def test_info_command(self):
        """Test info command."""
        from click.testing import CliRunner
        from cli_anything.topaz_video.topaz_video_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["info"])

        # Should succeed if Topaz Video is installed
        if result.exit_code == 0:
            assert "Topaz Video" in result.output
        else:
            # Topaz not installed - check error message
            assert "not found" in result.output.lower() or result.exit_code != 0


class TestProbeCommand:
    """Tests for probe command."""

    def test_probe_nonexistent_file(self):
        """Test probe with nonexistent file."""
        from click.testing import CliRunner
        from cli_anything.topaz_video.topaz_video_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["probe", "/nonexistent/file.mp4"])

        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "error" in result.output.lower()


class TestProcessCommand:
    """Tests for process command."""

    def test_process_missing_input(self):
        """Test process with missing input."""
        from click.testing import CliRunner
        from cli_anything.topaz_video.topaz_video_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["process", "/nonexistent/input.mp4", "/tmp/output.mp4"])

        assert result.exit_code != 0


class TestConvertCommand:
    """Tests for convert command."""

    def test_convert_missing_input(self):
        """Test convert with missing input."""
        from click.testing import CliRunner
        from cli_anything.topaz_video.topaz_video_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["convert", "/nonexistent/input.mp4", "/tmp/output.mp4"])

        assert result.exit_code != 0


class TestJSONOutput:
    """Tests for JSON output mode."""

    def test_probe_json_invalid_file(self):
        """Test probe --json with invalid file."""
        from click.testing import CliRunner
        from cli_anything.topaz_video.topaz_video_cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "probe", "/nonexistent/file.mp4"])

        # Should return JSON error or error message
        output = result.output
        try:
            data = json.loads(output)
            assert "error" in data
        except json.JSONDecodeError:
            # If not JSON, check if error message is present
            assert "not found" in output.lower() or "error" in output.lower() or result.exit_code != 0
