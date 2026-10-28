#!/usr/bin/env sh
cd "$(dirname "$0")" || exit 1
exec python3 "fusion_stage12/vlab_r18_http_ui.py"
