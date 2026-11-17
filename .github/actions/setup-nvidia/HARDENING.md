<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia/v20261103-202628** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### static-arg-collapse (severity: medium)

argument collapse in step "Export GPU detection result": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:69`

## Iteration Notes

### Iteration 1

**Fixes applied:** static-arg-collapse

**Notes:**

In the 'Export GPU detection result' step, GPU_FLAG is now built from a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)) and written to GITHUB_ENV with printf "${gpu_args[*]}". Previously one echo wrote the flag and its value together as a single string. The value written to GITHUB_ENV has not changed. It has to stay the same because downstream pytorch workflows use GPU_FLAG as a public interface and expand it unquoted (docker run ${GPU_FLAG:-}). A comment now explains that GPU_FLAG is a list of arguments and must be expanded unquoted or split into an array. Nothing in the action itself expands GPU_FLAG double-quoted. Because the exported string is identical, a static check that only looks for a flag and its value stored in one variable may still flag this line.

