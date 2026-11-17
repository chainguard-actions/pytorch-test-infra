<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261027-001733** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step uses a branch ref instead of a full commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:95`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV. The script does not set RUNNER_TEMP itself. The writes are `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"` and the same pattern for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. None of them run `printf '%s' ... | tr -d '\n\r'` first. RUNNER_TEMP is normally set by the runner. The check treats any env var a composite action inherits as workflow-controlled, so these writes need the sanitization step.

Locations:

- `action.yml:63`
- `action.yml:68`
- `action.yml:73`

### static-arg-collapse (severity: medium)

argument collapse in step "Set GPU_FLAG if in a container that has a NVIDIA GPU": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:99`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection, static-arg-collapse

**Notes:**

I fixed all three findings in action.yml.

1. unpinned-uses: `pytorch/test-infra/.github/actions/setup-nvidia@main` is now pinned to the upstream commit this mirror was built from, `9206d491d3a5507163cb9d5b77040d4c3ef5e038` (checked with lookup_action_sha). The `# main` comment is kept for readability.

2. github-env-injection: the step now strips newlines from RUNNER_TEMP once, using `printf '%s' | tr -d '\n\r'`, and strips them again from each directory path just before it is written to GITHUB_ENV. The paths are unchanged under normal conditions.

3. static-arg-collapse: GPU_FLAG is now built from a bash array (`--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all`) and joined with spaces when written to GITHUB_ENV, so the value is exactly what it was. I did not split it into separate env vars: workflows that call this action expect one GPU_FLAG and expand it unquoted in `docker run`, which splits it into separate arguments, so changing its form would break them. A rerun of the check may still flag this, since the written value is the same flag-plus-value string.

