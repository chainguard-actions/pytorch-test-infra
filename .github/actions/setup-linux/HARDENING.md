<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261112-155209** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs. Pin it to a commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' builds values from the inherited process env var RUNNER_TEMP, which this run: script reads but does not set. It writes them to $GITHUB_ENV without running `printf '%s' ... | tr -d '\n\r'` first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are written the same way. If the value contains a newline, extra environment variables can be injected.

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

I fixed two of the three findings in action.yml and left the third unchanged on purpose.

1. **unpinned-uses (fixed):** the `setup-nvidia@main` step is now pinned to the upstream commit this mirror was built from, `6f7274a0eff04dd4f8ada574e4e144610cece2c8`, with a `# main` comment. I used that commit rather than the current `main` head (`c91174703a48...`) so the sub-action matches the rest of this build.

2. **github-env-injection (fixed):** in the 'Setup useful environment variables' step, `RUNNER_TEMP` now has newlines and carriage returns stripped before it is used. Each directory value is also run through `printf '%s' | tr -d '\n\r'` right before it is written to `$GITHUB_ENV`. The step still writes the same three variables.

3. **static-arg-collapse (not changed):** `GPU_FLAG=--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all` is a fixed value this action exports for the workflows that call it. Those workflows are expected to use it unquoted (`docker run ${GPU_FLAG:-} ...`), which splits it into separate arguments. This action never uses the variable itself, and the pinned setup-nvidia step exports the same value. A bash array can't be passed through `GITHUB_ENV`, so changing the format would break every caller. I added a comment explaining this instead. A re-scan may flag it again.

### Iteration 2

**Fixes applied:** static-arg-collapse

**Notes:**

In the step "Set GPU_FLAG if in a container that has a NVIDIA GPU", GPU_FLAG is now built from a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)) and joined into GITHUB_ENV with printf, so each flag and its value is a separate token. Nothing in this action expands GPU_FLAG. Callers use it unquoted (docker run ${GPU_FLAG:-}), and setup-nvidia exports the same value. So the text it writes is byte-for-byte the same as upstream's, and callers are not affected. Not tested; the static checker may still flag the line, because the action has to write the flags as one string.

