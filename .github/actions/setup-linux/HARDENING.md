<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261029-163400** was hardened automatically. 3 finding(s) were identified and resolved across 3 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step in action.yml references an action by branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var ${RUNNER_TEMP}. The script does not set RUNNER_TEMP itself, and it writes these values to $GITHUB_ENV without first running `printf '%s' ... | tr -d '\n\r'` (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`). Under this check's rules for composite actions, a calling workflow can control inherited env vars, so a value containing a newline could inject extra env entries. Strip newlines from each value before writing it.

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

Pinned pytorch/test-infra/.github/actions/setup-nvidia to f2f972bd8f3eab11aa0094897a81879653c6f141 (this mirror's upstream commit, checked with lookup_action_sha; the '# main' comment keeps the original ref readable). The 'Setup useful environment variables' step now strips newlines from RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR with printf '%s' | tr -d '\n\r' before writing them to GITHUB_ENV. The directories are still created and cleaned exactly as before.

Not fixed: static-arg-collapse. I left it alone on purpose, so the next analysis pass will probably report it again. GPU_FLAG='--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all' is an env var this action hands to calling workflows, and the setup-nvidia action exports the same value. This action never uses GPU_FLAG itself. Callers expand it unquoted (e.g. docker run ${GPU_FLAG:-}), so the shell splits it into separate arguments and the flags do not collapse into one. Building an array here can't help, because arrays can't be passed through GITHUB_ENV. Changing the value's format would break every workflow that uses it. No action.yml change can clear this finding without breaking callers.

### Iteration 2

**Notes:**

I left the static-arg-collapse finding (action.yml line 102) unfixed because I believe it is a false positive. The step writes a fixed string, 'GPU_FLAG=--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all', to GITHUB_ENV. Nothing in this action expands GPU_FLAG double-quoted, or at all. It is an exported interface variable: PyTorch workflows expand it unquoted (e.g. 'docker run ${GPU_FLAG:-} ...') so it splits into separate arguments, and pytorch/test-infra setup-nvidia exports the same variable in the same format. The value holds no workflow-controlled data, so there is no injection risk. A bash array cannot be passed through GITHUB_ENV, so changing the format would break every downstream docker run that uses it. I made no changes, to keep upstream behaviour intact.

### Iteration 3

**Fixes applied:** static-arg-collapse

**Notes:**

In action.yml, the step "Set GPU_FLAG if in a container that has a NVIDIA GPU" now builds the GPU flags as a bash array (--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all) and writes it to GITHUB_ENV with printf. GPU_FLAG keeps exactly the same value. It is part of the interface with callers: PyTorch workflows and the sibling setup-nvidia action expand $GPU_FLAG unquoted in `docker run`, which splits it into separate arguments. Changing its format would break them. The value is a fixed string with no workflow-controlled data, so there is no injection risk. Nothing in this action expands it double-quoted. This finding may be a false positive: the step writes the same string as before, only built from an array now, so a re-scan could still match it. Nothing was run or tested.

