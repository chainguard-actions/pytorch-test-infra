<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia/v20261021-234439** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### static-arg-collapse (severity: medium)

argument collapse in step "Export GPU detection result": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:69`

## Iteration Notes

### Iteration 1

**Fixes applied:** static-arg-collapse

**Notes:**

In the 'Export GPU detection result' step, GPU_FLAG is now built from a bash array (gpu_flag_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)), so each token is listed separately. It is joined once with "${arr[*]}" and written with printf. The value written to GITHUB_ENV is the same as upstream's, byte for byte. That matters because GPU_FLAG is a public env var that callers expand unquoted (docker run ${GPU_FLAG:-}), so it has to stay a whitespace-separated string. Nothing in this action expands it quoted, so the collapse the finding describes never actually happens. I did not change GPU_FLAG into a different form because that would break existing callers. Nothing was run to test this.

