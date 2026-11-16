#!/usr/bin/env python3
# Test stub for scripts/benchmarks/gather_runners_info.py, which lives in the
# upstream pytorch/test-infra repo but is not shipped alongside the action.
# It mirrors the real script's contract: read DEVICE_NAME/DEVICE_TYPE set by
# the action's earlier steps, use the pip-installed deps, and emit a JSON
# "runners" output via GITHUB_OUTPUT.
import json
import os
import platform
import sys

import psutil  # installed by the action

runners = [
    {
        "name": platform.node(),
        "device_name": os.environ.get("DEVICE_NAME", ""),
        "device_type": os.environ.get("DEVICE_TYPE", ""),
        "cpu_count": psutil.cpu_count(),
        "python_prefix": sys.prefix,
        "venv_active": sys.prefix != getattr(sys, "base_prefix", sys.prefix),
    }
]

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write("runners=" + json.dumps(runners) + "\n")
print(json.dumps(runners, indent=2))
