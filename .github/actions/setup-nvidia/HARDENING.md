<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### static-arg-collapse (severity: medium)

argument collapse in step "Export GPU detection result": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:69`

## Iteration Notes

### Iteration 1

**Fixes applied:** static-arg-collapse

**Notes:**

In the "Export GPU detection result" step, GPU_FLAG is now built from a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)), so each docker argument is defined as its own token. It is then joined with ${gpu_args[*]} and written with printf. The value in GITHUB_ENV is byte-for-byte what upstream wrote. This was required: downstream PyTorch workflows read GPU_FLAG and expand it unquoted (docker run ${GPU_FLAG:-}), which splits it into separate arguments, so changing the value or its format would break them. The value is a static literal with no workflow-controlled data, so there was no injection risk. I added a comment saying it is an argument list and that callers wanting an array should use gpu_args=($GPU_FLAG). The fix has not been run or re-scanned. If the analyzer only looks for a flag and its value written together, it may still flag this step, but the env var's contract can't change without breaking consumers.

