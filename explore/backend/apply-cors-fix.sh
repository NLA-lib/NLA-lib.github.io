#!/usr/bin/env bash
# Apply the preflight fix to the existing package, then update the healthy stack.
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c auth.zip.sha256
python3 patch_archive.py
bash ./deploy.sh
