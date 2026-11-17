<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite action step points to a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this step runs.

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

Pinned pytorch/test-infra/.github/actions/setup-nvidia@main to e9b5b0a4c36ebfde49dec880ae77705038009471 (# main). This is the upstream commit this mirror version was built from, and I confirmed it resolves in pytorch/test-infra.

static-arg-collapse: GPU_FLAG is a public value that downstream PyTorch workflows (and setup-nvidia itself) read. They expand it without quotes, as `docker run ${GPU_FLAG:-}`, so the shell splits it into separate arguments. Splitting it into separate env entries would break every consumer. So the step now builds the flags as a bash array, one token per element (`gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)`), and writes the value with printf. The value is still the same space-separated string. The value is a fixed literal with no user input in it, so nothing can be injected. A comment in the step explains the contract and says consumers must not double-quote the value. If the analyzer still flags this pattern, treat it as an accepted exception: changing the value's format would break downstream workflows.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Setup useful environment variables' step of action.yml, each value built from RUNNER_TEMP (RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR, RUNNER_DOCS_DIR) now goes through printf '%s' ... | tr -d '\n\r' before it is written to $GITHUB_ENV. Directory creation and cleanup still use the original paths. On a normal runner RUNNER_TEMP never contains newlines, so the values written are unchanged. No test was run.

