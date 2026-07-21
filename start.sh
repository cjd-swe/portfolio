#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="$PROJECT_ROOT/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Error: $PYTHON_BIN was not found. Install Python 3.12 or newer." >&2
    exit 1
fi

if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)'; then
    echo "Error: Python 3.12 or newer is required (found $("$PYTHON_BIN" --version 2>&1))." >&2
    exit 1
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "Creating virtual environment..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

if ! "$VENV_PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)'; then
    echo "Error: .venv uses an unsupported Python version." >&2
    echo "Remove .venv and run this script again to recreate it." >&2
    exit 1
fi

echo "Installing dependencies..."
"$VENV_PYTHON" -m pip install --disable-pip-version-check -r requirements.txt

if [[ ! -f .env ]]; then
    SECRET_KEY="$($VENV_PYTHON -c 'import secrets; print(secrets.token_urlsafe(50))')"
    printf 'DJANGO_SECRET_KEY=%s\nDJANGO_DEBUG=True\n' "$SECRET_KEY" > .env
    echo "Created .env with local development settings."
else
    echo "Using existing .env."
fi

echo "Applying database migrations..."
"$VENV_PYTHON" manage.py migrate

if [[ $# -eq 0 ]]; then
    echo "Starting Django at http://127.0.0.1:8000/"
else
    echo "Starting Django with arguments: $*"
fi
exec "$VENV_PYTHON" manage.py runserver "$@"
