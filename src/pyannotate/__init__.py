# File: src/pyannotate/__init__.py

"""pyannotate package init.
This package provides functionality to automatically add or update file headers
in various programming language files.
"""

from __future__ import annotations

__all__ = ["__version__"]

# Prefer stdlib 'importlib.metadata'; fall back to the backport if needed.
try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _get_version
except ImportError:  # pragma: no cover - for very old Python only
    try:
        from importlib_metadata import PackageNotFoundError
        from importlib_metadata import version as _get_version  # type: ignore
    except ImportError:  # pragma: no cover - metadata unavailable
        _get_version = None  # type: ignore[assignment]

        class PackageNotFoundError(Exception):  # type: ignore[no-redef]
            """Placeholder when importlib metadata is unavailable."""


def _read_version() -> str:
    """Best-effort package version without broad exception catches."""
    if _get_version is None:  # metadata API unavailable
        return "0.0.0"
    try:
        return _get_version("pyannotate")  # type: ignore[operator]
    except PackageNotFoundError:
        return "0.0.0"


__version__ = _read_version()
