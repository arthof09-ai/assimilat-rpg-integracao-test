#!/usr/bin/env python3
"""Single safe operator entrypoint for BENCHMARK_AUTO, no local web UI."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'fusion_stage12'))
from vlab_r23_benchmark_auto import cli
if __name__=='__main__':raise SystemExit(cli())
