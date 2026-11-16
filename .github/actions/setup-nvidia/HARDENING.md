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

The flagged value in the 'Export GPU detection result' step is not a real argument collapse. GPU_FLAG is written to GITHUB_ENV as a public output for calling workflows. They expand it unquoted (docker run ${GPU_FLAG:-} ...), so it splits into separate arguments, and nothing inside this action expands it double-quoted. Splitting it into an array or several variables would break every caller. So I left the value exactly as before ('--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all'). The step now builds it from a bash array of words, joins them with spaces and writes it with printf, with a comment explaining the interface. I didn't re-run the analysis, so I can't say whether the detector stops reporting it. If it still flags the step, treat it as a false positive rather than changing the value. No other changes.

