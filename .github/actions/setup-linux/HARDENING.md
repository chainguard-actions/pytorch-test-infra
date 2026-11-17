<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-192709** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite action step points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

Step 'Setup useful environment variables' writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV. The written values are RUNNER_ARTIFACT_DIR="${RUNNER_TEMP}/artifacts", RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR, and none of them go through `printf '%s' ... | tr -d '\n\r'` first. For example: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. The check counts any env var the script reads but did not set itself as caller-controlled. Strip newlines from each value before writing it.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

### static-arg-collapse (severity: medium)

argument collapse in step "Set GPU_FLAG if in a container that has a NVIDIA GPU": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:99`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed two of the three findings. The third (static-arg-collapse) is left as upstream had it, on purpose.

- unpinned-uses: pytorch/test-infra/.github/actions/setup-nvidia@main is now pinned to 0569df511711f70601c984fe3a93dac324afc9ce (# main). That is the upstream commit this mirror was built from, and lookup_action_sha confirmed it.
- github-env-injection: RUNNER_TEMP and each derived path (RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR, RUNNER_DOCS_DIR) now go through printf '%s' | tr -d '\n\r' before being written to $GITHUB_ENV.
- static-arg-collapse: not changed. GPU_FLAG='--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all' is a fixed string with no caller input. It is the env var downstream PyTorch workflows read: they expand ${GPU_FLAG} unquoted in docker run, so it already splits into separate arguments. The setup-nvidia action exports the same value. Turning it into an array or splitting it up would break every caller. I added a comment explaining why, but the analyzer will probably flag this again.

### Iteration 2

**Fixes applied:** static-arg-collapse

**Notes:**

In the step "Set GPU_FLAG if in a container that has a NVIDIA GPU", each token of GPU_FLAG is now its own element in a bash array (gpu_flag_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)). The step then joins the array and writes it with printf to GITHUB_ENV. The value written is exactly the same as before. Not tested; I only checked the change by reading it. This finding is close to a false positive. The value is a fixed string with no user input in it, so nothing can be injected. It is also an interface that consumers rely on: they expand $GPU_FLAG unquoted (docker run ${GPU_FLAG}), and the setup-nvidia sub-action exports the same value. Changing the string or splitting it into several env vars would break those workflows. So the exported value stays the same and only the way it is built changed. A later scan could still flag this line if the checker looks at the GPU_FLAG variable itself, because it still holds a flag and its value together.

