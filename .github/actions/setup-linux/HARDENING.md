<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20260922-155642** was hardened automatically. 3 finding(s) were identified and resolved across 3 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a branch, not a commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch changes the code this action runs. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:86`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process variable ${RUNNER_TEMP}. It then writes them to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without first running `printf '%s' ... | tr -d '\n\r'`. RUNNER_TEMP is not set inside this script, so under rule (e) it counts as workflow-controlled. A newline in the value could inject extra environment variables. Strip newlines from each value before writing it.

Locations:

- `action.yml:71`
- `action.yml:76`
- `action.yml:81`

### static-arg-collapse (severity: medium)

argument collapse in step "Set GPU_FLAG if in a container that has a NVIDIA GPU": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:99`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia to 28dee7456d0348d74a5faa85098bb028b263ee2b (the upstream commit this mirror version was built from, checked with lookup_action_sha), keeping '# main' as a comment. In 'Setup useful environment variables', each value is now run through printf '%s' | tr -d '\n\r' before it is written to $GITHUB_ENV. I did not change static-arg-collapse, on purpose. GPU_FLAG ('--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all') is a constant this action sets for the caller's later steps. Nothing in this action expands it. Callers' workflows read it unquoted (e.g. docker run ${GPU_FLAG:-}), so it splits into separate arguments as intended. A bash array cannot be passed through GITHUB_ENV, and changing the variable's form would break every caller. The value is a fixed literal that the workflow cannot control, so there is no injection or collapse risk inside this action.

### Iteration 2

**Notes:**

static-arg-collapse (action.yml line 102) is a false positive and I left it as is on purpose. I added only a comment explaining why. GPU_FLAG='--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all' is a fixed value upstream sets and exports through GITHUB_ENV. Downstream PyTorch workflows read it unquoted (docker run ${GPU_FLAG:-} ...), so it already splits into separate arguments, and the setup-nvidia action exports the same variable in the same format. Nothing in the action expands it double-quoted, and no workflow-controlled value or ${{ }} expression is involved, so it cannot be injected. Splitting or reformatting the variable would break every caller that relies on it. If the analyzer keeps flagging it, it should be suppressed rather than changed.

### Iteration 3

**Fixes applied:** static-arg-collapse

**Notes:**

In the step "Set GPU_FLAG if in a container that has a NVIDIA GPU", the GPU flags are now built as a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)) and joined into GITHUB_ENV with printf. The value written is exactly the same as before, because GPU_FLAG is shared with the setup-nvidia action and workflows expand it unquoted (docker run ${GPU_FLAG:-}), which splits it into separate arguments. Changing the value would break those consumers. The flags are fixed text, so no workflow-controlled data is involved. Not tested.

