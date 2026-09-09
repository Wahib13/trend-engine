#!/usr/bin/env bash
#
# Server-side backend deploy. Piped to the server over SSH by
# .github/workflows/deploy.yml and run with `bash -s`.
#
# The built UI is uploaded separately by the workflow (rsync), so this script
# does NOT touch node/npm or the web root.
#
# Config is supplied by the CI job as environment variables:
#   DEPLOY_PATH  - repo checkout on the server (e.g. /home/deploy/trend-engine)
#   API_SERVICE  - systemd unit for the API (e.g. trend-engine-api)
#   VENV_PATH    - optional; defaults to $DEPLOY_PATH/.venv
set -euo pipefail

: "${DEPLOY_PATH:?DEPLOY_PATH not set}"
: "${API_SERVICE:?API_SERVICE not set}"
VENV_PATH="${VENV_PATH:-$DEPLOY_PATH/.venv}"

echo "==> Deploying in $DEPLOY_PATH"
cd "$DEPLOY_PATH"

echo "==> Fetching latest main"
git fetch --prune origin
# Hard reset avoids merge conflicts on the server; the server tree is a
# deploy artifact, not a place to make edits.
git reset --hard origin/main

echo "==> Installing Python deps + running migrations"
# shellcheck disable=SC1091
source "$VENV_PATH/bin/activate"
# torch's Linux wheel (with CUDA deps) is multi-GB; pip extracts into TMPDIR,
# and the default /tmp here is a small (2G) tmpfs. Point it at the real disk.
PIP_TMPDIR="$DEPLOY_PATH/.pip-tmp"
mkdir -p "$PIP_TMPDIR"
TMPDIR="$PIP_TMPDIR" pip install -r requirements.txt
# alembic.ini and env.py live in src/; env.py reads DATABASE_CONNECTION_STRING
# from ../.env, so migrations must run from src/ on the server.
( cd src && alembic upgrade head )

echo "==> Restarting API service ($API_SERVICE)"
sudo systemctl restart "$API_SERVICE"

echo "==> Backend deploy complete"
