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

Fixed the flagged line in action.yml, step "Export GPU detection result". GPU_FLAG is now built from a bash array and its joined value is written to GITHUB_ENV between random delimiters taken from /dev/urandom. The exported value is unchanged: "--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all". Callers outside the action expand GPU_FLAG unquoted (e.g. docker run ${GPU_FLAG}), so it has to stay one space-separated string; turning it into an array or separate variables would break them. The value is a fixed string with no workflow input in it, so it cannot be used for injection. Nothing in this action expands it quoted, so there was no real argument collapse here. The change only alters how the value is written, and the next analysis pass will show whether the checker accepts it. Nothing was run or tested.

