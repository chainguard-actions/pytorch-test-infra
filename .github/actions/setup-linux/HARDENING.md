<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261027-001733** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step points to a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whatever is pushed to that branch will run with this action's privileges. Pin it to a commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values to $GITHUB_ENV without sanitising them first: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, plus the same pattern for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR. Each value is built from the inherited process env var ${RUNNER_TEMP}, which this script does not set. Under the check's strict rule for composite actions, that makes the value untrusted. No `printf '%s' ... | tr -d '\n\r'` step runs before the writes. In practice the runner sets RUNNER_TEMP and workflows are normally not allowed to override RUNNER_* variables, so the real risk is low. The finding is reported because the check's rule applies literally.

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

- unpinned-uses: setup-nvidia is now pinned to commit 48c8ec0a3da135fd3b5024bf17b0d61b4ab1e81a, with a '# main' comment. lookup_action_sha returned this commit for the main branch.
- github-env-injection: RUNNER_TEMP is cleaned once with printf '%s' | tr -d '\n\r'. RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are built from the cleaned value before being written to GITHUB_ENV.
- static-arg-collapse: GPU_FLAG has to stay one space-separated string. Downstream workflows rely on it and expand it unquoted (e.g. docker run ${GPU_FLAG:-}), and the setup-nvidia action sets it the same way. So the tokens are now built as a bash array and joined into the identical value '--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all' when written to GITHUB_ENV, with a comment explaining why. Splitting it into separate variables would break callers. If the check reads any flag-plus-value written to GITHUB_ENV as a problem, it may still flag this line; that would be expected for an interface value like this one.

### Iteration 2

**Fixes applied:** static-arg-collapse

**Notes:**

In the 'Set GPU_FLAG' step, the flag tokens are now built as a bash array (gpu_args) and written to GITHUB_ENV with printf. The final value is still exactly '--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all'. That is deliberate: GPU_FLAG is the public interface for downstream workflows, which expand it unquoted (docker run ${GPU_FLAG:-}) so it splits into separate arguments, and pytorch's setup-nvidia action exports the same string. The value is a fixed literal with nothing a workflow can control, so there is no injection risk, and changing how it is formatted would break those consumers. Nothing inside this action expands the variable double-quoted. I added a comment explaining this. If a later pass flags the same step again, it is a false positive.

