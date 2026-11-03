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

In the "Export GPU detection result" step, the GPU flags (--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all) are now built as a bash array called gpu_args. Two environment variables come from that array:
- GPU_FLAG has exactly the same value as upstream. Downstream pytorch workflows use it unquoted (docker run ${GPU_FLAG}) and rely on the shell splitting it into separate arguments, so changing it would break them. The value is a fixed string with no input from the workflow, so it can't be used for injection.
- GPU_FLAG_ARGS is new and holds one token per line. It's written with a random heredoc delimiter, so callers who want quoted arguments can load it into an array without one argument swallowing the others.

The change hasn't been run or re-analyzed. A static check that matches any flag-plus-value stored in one variable may still flag GPU_FLAG. Keeping it was deliberate: removing it or splitting its value would break every downstream caller. Nothing else in action.yml changed.

