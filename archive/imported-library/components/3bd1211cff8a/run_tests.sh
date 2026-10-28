#!/bin/sh
set -eu
cd "$(dirname "$0")"
python -m unittest discover -s reference_r39 -p test_r39_version_gate.py -q
python -m unittest discover -s . -p test_r39a_inline_alternantes.py -q
