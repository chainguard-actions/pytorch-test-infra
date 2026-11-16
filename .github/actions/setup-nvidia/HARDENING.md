<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia/v20261029-163400** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### static-arg-collapse (severity: medium)

argument collapse in step "Export GPU detection result": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:69`

## Iteration Notes

### Iteration 1

**Fixes applied:** static-arg-collapse

**Notes:**

In the 'Export GPU detection result' step, GPU_FLAG is now built from a bash array (--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all) and joined into one string with "${gpu_args[*]}" before it is written to GITHUB_ENV. The exported value is byte-for-byte the same as upstream's. That matters because downstream workflows expand GPU_FLAG unquoted (docker run ${GPU_FLAG} ...), which splits it into separate arguments, and changing the value would break them. Nothing in this action expands the variable inside double quotes, so the 'one argument' problem never actually happens here. The value is a constant with nothing user-controlled in it. A comment in the step explains this.

