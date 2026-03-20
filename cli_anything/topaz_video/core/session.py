"""Session management for Topaz Video CLI.

This module manages the CLI session state and history.
"""

import json
import os
from pathlib import Path
from typing import Optional


class Session:
    """Represents a CLI session with state."""

    def __init__(self, working_dir: Optional[str] = None):
        self.working_dir = working_dir or os.getcwd()
        self.current_project = None
        self.history = []

    def set_working_dir(self, path: str) -> None:
        """Set the working directory."""
        self.working_dir = path

    def set_project(self, project_name: str) -> None:
        """Set the current project."""
        self.current_project = project_name

    def add_history(self, command: str) -> None:
        """Add a command to history."""
        self.history.append({
            "command": command,
            "timestamp": str(Path(__file__).stat().st_mtime)
        })

    def to_dict(self) -> dict:
        """Convert session to dictionary."""
        return {
            "working_dir": self.working_dir,
            "current_project": self.current_project,
            "history": self.history,
        }

    def save(self, path: str) -> None:
        """Save session to file."""
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "Session":
        """Load session from file."""
        with open(path) as f:
            data = json.load(f)

        session = cls(working_dir=data.get("working_dir"))
        session.current_project = data.get("current_project")
        session.history = data.get("history", [])
        return session


def get_default_session_path() -> str:
    """Get the default session file path."""
    home = Path.home()
    session_dir = home / ".cli-anything" / "topaz_video"
    session_dir.mkdir(parents=True, exist_ok=True)
    return str(session_dir / "session.json")
