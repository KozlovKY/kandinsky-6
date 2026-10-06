"""Default directory for weights, logs, exports, profiles, and generated videos.

``KANDINSKY_HOME`` overrides the root. Unset, the root is ``~/.cache/kandinsky``.
An explicit CLI path or config field still wins over these defaults.

Experiment runs live under ``outputs/<name>_<YYYY-MM-DDTHH-MM-SS>/`` with
``launch.json``, ``generations/``, ``logs/``, and ``profiles/``. ``KANDINSKY_LOG_DIR``
and ``KANDINSKY_PROFILE_DIR`` point a process at one run's logs and profiles.
"""

from __future__ import annotations

import os
from pathlib import Path


def kandinsky_home() -> Path:
    raw = os.environ.get("KANDINSKY_HOME")
    if raw:
        return Path(os.path.expandvars(os.path.expanduser(raw)))
    return Path.home() / ".cache" / "kandinsky"


def weights_dir() -> Path:
    return kandinsky_home() / "weights"


def logs_dir() -> Path:
    override = os.environ.get("KANDINSKY_LOG_DIR")
    if override:
        return Path(os.path.expandvars(os.path.expanduser(override)))
    return kandinsky_home() / "logs"


def export_dir() -> Path:
    return kandinsky_home() / "export"


def output_dir() -> Path:
    return kandinsky_home() / "output"


def outputs_dir() -> Path:
    """Root for experiment runs. One subdirectory per launch."""
    return kandinsky_home() / "outputs"


def profile_dir() -> Path:
    override = os.environ.get("KANDINSKY_PROFILE_DIR")
    if override:
        return Path(os.path.expandvars(os.path.expanduser(override)))
    return kandinsky_home() / "profile"
