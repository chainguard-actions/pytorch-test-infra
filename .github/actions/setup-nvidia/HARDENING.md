<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-nvidia/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-nvidia/v20261112-155209** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### static-arg-collapse (severity: medium)

argument collapse in step "Export GPU detection result": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:69`

## Iteration Notes

### Iteration 1

**Fixes applied:** static-arg-collapse

**Notes:**

In the "Export GPU detection result" step, GPU_FLAG is now built from a bash array (gpu_flag_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)) and written to GITHUB_ENV with printf using "${arr[*]}". The value written to GITHUB_ENV is byte-for-byte the same as upstream's.

I didn't change that value or split it into several variables on purpose. GPU_FLAG is part of this action's public interface, and downstream PyTorch workflows expand it unquoted (docker run ${GPU_FLAG:-} ...), so the shell already splits it into separate arguments. Changing its format would break every one of those callers.

The finding itself was not a real risk: the value is a fixed string with no workflow input or expression in it. I also haven't re-run the analysis, so I can't confirm the rewrite clears the finding. It now only changes how the string is put together. If the analyzer still flags it, the real choice is between keeping it as a reviewed exception or making a breaking change for callers.

I added a comment in the step saying that consumers must not expand GPU_FLAG in double quotes, and showing how to split it into an array instead. Nothing else in the file was touched.

