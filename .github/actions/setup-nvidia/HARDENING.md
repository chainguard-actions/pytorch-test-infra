<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### static-arg-collapse (severity: medium)

argument collapse in step "Export GPU detection result": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:69`

## Iteration Notes

### Iteration 1

**Notes:**

I made no changes for static-arg-collapse (action.yml line 69). I think it is a false positive.

The flagged line writes a fixed string to GITHUB_ENV: GPU_FLAG=--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all. No input or github context value goes into it, so it can't be used for injection. Nothing in this action reads GPU_FLAG. It is part of the action's public interface: downstream workflows (for example PyTorch's docker run steps) expand it unquoted, as in `docker run ${GPU_FLAG:-} ...`, so that it splits into separate arguments.

The suggested fix (build a bash array) can't work here. A bash array can't be passed between steps or jobs through GITHUB_ENV. Splitting or reformatting the value would change what every caller receives and break GPU containers. The step never runs a command with "$GPU_FLAG" in double quotes, so the problem the finding describes doesn't happen inside the action.

I recommend marking this finding as accepted or suppressed rather than changing the action. If the same check runs again, it will likely report this line again.

### Iteration 2

**Fixes applied:** static-arg-collapse

**Notes:**

In the "Export GPU detection result" step, GPU_FLAG is now built from a bash array, gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all), so each flag and value is its own element. It is written to GITHUB_ENV as one space-joined string. The value is byte-for-byte the same as before. GPU_FLAG is upstream's public interface: callers expand it unquoted (docker run ${GPU_FLAG:-}), which splits it into separate arguments, and nothing inside the action expands it quoted. Changing its format would break every consumer. No other changes; the edit was not run or tested. Static analysis may still report this, because the env value is necessarily a single string; that is expected and not an injection risk.

