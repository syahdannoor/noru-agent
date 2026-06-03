#!/usr/bin/env bash
# Noru Agent CLI - shell wrapper for Git Bash / MSYS on Windows
# Installed by: scripts/install.sh
# Usage: noru [options...]

export NORU_HOME="${NORU_HOME:-$HOME/AppData/Local/noru}"
export HERMES_HOME="${NORU_HOME}"

# Locate the noru-agent repo
NORU_REPO="${NORU_REPO:-$HOME/noru-agent}"
if [ ! -d "$NORU_REPO" ]; then
    # Fallback: check if installed alongside hermes
    NORU_REPO="$HOME/.noru/noru-agent"
fi

if [ -d "$NORU_REPO/venv" ]; then
    source "$NORU_REPO/venv/Scripts/activate" 2>/dev/null
fi

PYTHONPATH="$NORU_REPO:$PYTHONPATH" exec python3 -m noru_cli.main "$@"
