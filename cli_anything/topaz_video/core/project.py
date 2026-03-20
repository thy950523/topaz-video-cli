"""Video project management.

This module manages video processing jobs and settings.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class VideoProject:
    """Represents a video processing job/project."""

    def __init__(
        self,
        name: str,
        input_path: str,
        output_path: Optional[str] = None,
        model: str = "enhance",
        scale: int = 2,
        settings: Optional[dict] = None
    ):
        self.name = name
        self.input_path = input_path
        self.output_path = output_path or self._default_output(input_path)
        self.model = model
        self.scale = scale
        self.settings = settings or {}
        self.created_at = datetime.now().isoformat()
        self.status = "created"

    def _default_output(self, input_path: str) -> str:
        """Generate default output path."""
        path = Path(input_path)
        stem = path.stem
        ext = path.suffix
        return str(path.parent / f"{stem}_processed{ext}")

    def to_dict(self) -> dict:
        """Convert project to dictionary."""
        return {
            "name": self.name,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "model": self.model,
            "scale": self.scale,
            "settings": self.settings,
            "created_at": self.created_at,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VideoProject":
        """Create project from dictionary."""
        project = cls(
            name=data["name"],
            input_path=data["input_path"],
            output_path=data.get("output_path"),
            model=data.get("model", "enhance"),
            scale=data.get("scale", 2),
            settings=data.get("settings", {})
        )
        project.created_at = data.get("created_at", project.created_at)
        project.status = data.get("status", "created")
        return project


def create_project(
    name: str,
    input_path: str,
    output_path: Optional[str] = None,
    model: str = "enhance",
    scale: int = 2,
    **settings
) -> VideoProject:
    """Create a new video project."""
    return VideoProject(
        name=name,
        input_path=input_path,
        output_path=output_path,
        model=model,
        scale=scale,
        settings=settings
    )


def save_project(project: VideoProject, path: str) -> None:
    """Save project to a JSON file."""
    with open(path, "w") as f:
        json.dump(project.to_dict(), f, indent=2)


def load_project(path: str) -> VideoProject:
    """Load project from a JSON file."""
    with open(path) as f:
        data = json.load(f)
    return VideoProject.from_dict(data)


def list_projects(directory: str) -> list[VideoProject]:
    """List all projects in a directory."""
    projects = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            try:
                project = load_project(os.path.join(directory, filename))
                projects.append(project)
            except Exception:
                pass
    return sorted(projects, key=lambda p: p.created_at, reverse=True)
