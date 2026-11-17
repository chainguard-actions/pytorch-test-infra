<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has a composite step that references an action by branch, not by a full 40-char commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`.

Locations:

- `action.yml:90`

### static-arg-collapse (severity: medium)

argument collapse in step "Set GPU_FLAG if in a container that has a NVIDIA GPU": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:99`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, static-arg-collapse

**Notes:**

Both findings are addressed in action.yml.

1. unpinned-uses: I pinned pytorch/test-infra/.github/actions/setup-nvidia to f2f972bd8f3eab11aa0094897a81879653c6f141 and left a '# main' comment. That commit is the upstream_ref this mirror was built from, and lookup_action_sha confirmed it exists.

2. static-arg-collapse: Nothing inside this action expands GPU_FLAG; it only writes it to GITHUB_ENV. Downstream workflows use it unquoted (docker run ${GPU_FLAG:-} ...), so the shell splits it into separate arguments as intended. Changing the format of the variable would break those callers. The step now builds the value from a bash array of separate tokens (--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all) and writes it with printf. The value written to GITHUB_ENV is exactly the same as upstream's, so callers see no difference. A comment in the step explains that callers must keep expanding GPU_FLAG unquoted. If the analyzer flags the GITHUB_ENV write again, treat that as a false positive: GPU_FLAG is meant to be split by its consumers.

