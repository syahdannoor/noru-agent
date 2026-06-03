"""Resolve NORU_HOME for standalone skill scripts.

Skill scripts may run outside the Hermes process (e.g. system Python,
nix env, CI) where ``noru_constants`` is not importable.  This module
provides the same ``get_noru_home()`` and ``display_noru_home()``
contracts as ``noru_constants`` without requiring it on ``sys.path``.

When ``noru_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``noru_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``NORU_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from noru_constants import display_noru_home as display_noru_home
    from noru_constants import get_noru_home as get_noru_home
except (ModuleNotFoundError, ImportError):

    def get_noru_home() -> Path:
        """Return the Hermes home directory (default: ~/.hermes).

        Mirrors ``noru_constants.get_noru_home()``."""
        val = os.environ.get("NORU_HOME", "").strip()
        return Path(val) if val else Path.home() / ".hermes"

    def display_noru_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``noru_constants.display_noru_home()``."""
        home = get_noru_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
