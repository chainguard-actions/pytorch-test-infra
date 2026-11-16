<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261103-202628** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step pins this action to a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`.

Locations:

- `action.yml:91`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds values from the inherited process env var RUNNER_TEMP. This script never sets RUNNER_TEMP, so the calling workflow controls it. The step then writes the values to $GITHUB_ENV without first running them through `printf '%s' ... | tr -d '\n\r'`. The writes are `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` plus the same pattern for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR.

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

Pinned pytorch/test-infra/.github/actions/setup-nvidia to e9b5b0a4c36ebfde49dec880ae77705038009471, the upstream commit this mirror was built from. I used that instead of main's current HEAD (a0cd4927...) so the nested action matches the rest of this release. The RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR values now pass through printf '%s' | tr -d '\n\r' before being written to $GITHUB_ENV.

static-arg-collapse is NOT fixed, on purpose. GPU_FLAG='--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all' is a public env var that callers' workflows expand unquoted (e.g. docker run ${GPU_FLAG}) so it splits into several arguments. The setup-nvidia sub-action sets the same variable in the same format. Nothing in this action expands it, so there is no collapse here to fix. Changing its format or splitting it up would break every downstream consumer, and a bash array cannot be passed through GITHUB_ENV. Expect this finding to come back on the next analysis pass.

### Iteration 2

**Fixes applied:** static-arg-collapse

**Notes:**

In the step "Set GPU_FLAG if in a container that has a NVIDIA GPU", the GPU flag tokens are now built as a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)) and written to GITHUB_ENV with printf as "${gpu_args[*]}". GPU_FLAG is a published environment variable that downstream PyTorch workflows expand unquoted in `docker run`, and that splits it into separate arguments. The value written is byte-for-byte the same as before, so callers keep working. The value was always a fixed string, so there was no injection risk. I didn't run the step to test it.

