<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-232755** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step refers to the action by a branch name, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. If that branch changes, the code this action runs changes with it. Pin it to a commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var ${RUNNER_TEMP}. The step does not set RUNNER_TEMP itself, so a calling workflow can control it. The step then writes these values to $GITHUB_ENV, for example `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, without first running `printf '%s' ... | tr -d '\n\r'` to strip newlines.

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

**Fixes applied:** unpinned-uses, github-env-injection, static-arg-collapse

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia to 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f, the upstream commit this mirror was built from, with a '# main' comment. The three RUNNER_* dir values now go through printf '%s' | tr -d '\n\r' before they are written to GITHUB_ENV. GPU_FLAG is now built from a bash array (gpu_flag_args) and written with printf. The exported value is still exactly '--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all'. That variable is a public interface: callers expand it unquoted and setup-nvidia sets it the same way, so changing its value would break them. The finding may still come back, because the value is still one string.

