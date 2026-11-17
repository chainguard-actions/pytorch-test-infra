<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### static-arg-collapse (severity: medium)

argument collapse in step "Export GPU detection result": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:69`

## Iteration Notes

### Iteration 1

**Fixes applied:** static-arg-collapse

**Notes:**

In the "Export GPU detection result" step, GPU_FLAG is now built from a bash array of separate tokens (--gpus, all, -e, NVIDIA_DRIVER_CAPABILITIES=all) and written to GITHUB_ENV with printf. The value is exactly what upstream wrote. GPU_FLAG is a documented environment variable that callers read, and pytorch workflows use it unquoted as ${GPU_FLAG:-} in docker run, which splits it into separate arguments, so changing its format would break them. I added a comment saying callers must expand it unquoted. This step never runs a command with GPU_FLAG itself, so it causes no argument collapse here. A later scan may still flag the variable, because one value still holds a flag together with its argument.

