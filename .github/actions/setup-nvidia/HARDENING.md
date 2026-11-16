<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### static-arg-collapse (severity: medium)

argument collapse in step "Export GPU detection result": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:69`

## Iteration Notes

### Iteration 1

**Fixes applied:** static-arg-collapse

**Notes:**

In the "Export GPU detection result" step, the docker GPU flags are now built as a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)), so each flag and its value is a separate token. GPU_FLAG is then written to GITHUB_ENV from "${gpu_args[*]}". The exported value is exactly the same as upstream's, because downstream pytorch workflows depend on it and expand it unquoted (docker run ${GPU_FLAG:-}). The value is a fixed constant and contains no user input, so nothing can be injected. I added a comment explaining how callers should use it. I have not re-run the analysis, so a pass that matches on the exported variable itself could still flag it.

