#!/usr/bin/env python3
"""Test stub for scripts/benchmarks/gather_runners_info.py.

Emits a minimal runners-info JSON to GITHUB_OUTPUT under the key "runners",
using the DEVICE_NAME / DEVICE_TYPE env vars set by earlier action steps.
"""
import json
import os
import platform

import psutil  # installed by the action; verifies the pip step worked

info = [
    {
        "name": os.environ.get("RUNNER_NAME", "act"),
        "type": os.environ.get("DEVICE_TYPE", ""),
        "device": os.environ.get("DEVICE_NAME", ""),
        "cpu_info": platform.processor() or platform.machine(),
        "cpu_count": psutil.cpu_count(),
        "avail_mem_in_gb": int(psutil.virtual_memory().total / (1024 ** 3)),
        "extra_info": {"stub": True},
    }
]

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"runners={json.dumps(info)}\n")
print(json.dumps(info))
