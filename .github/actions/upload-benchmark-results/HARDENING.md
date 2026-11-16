<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml pins composite steps to a mutable branch instead of a full 40-character commit SHA: line 31 `uses: pytorch/test-infra/.github/actions/setup-uv@main` and line 115 `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP comes from the process environment the composite action inherits, not from this script, and nothing strips newlines from it before the write. GitHub says workflows can't overwrite RUNNER_* variables, so the real risk is low, but the check counts any inherited variable. Fix: `safe=$(printf '%s' "$RUNNER_TEMP" | tr -d '\n\r')`, then write `VIRTUAL_ENV=${safe}/benchmark-upload-venv` to "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the two pytorch/test-infra sub-actions (setup-uv and get-workflow-job-id) to e9b5b0a4c36ebfde49dec880ae77705038009471. That is the upstream commit this mirror was built from, so the sub-actions stay at the same version as the parent action. I took the SHA from the request and did not run a lookup. In the 'Install dependencies' step, newlines are now stripped from RUNNER_TEMP before the VIRTUAL_ENV line is written to $GITHUB_ENV, and $GITHUB_ENV is now quoted. Nothing was run to test these changes.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Get device type' step of action.yml, DEVICE_TYPE is now sanitized with printf '%s' | tr -d '\n\r' before it is written to "$GITHUB_ENV", and the variable is now quoted. ${DEVICE_TYPE:-} keeps the step working if set -u is on. I did not reset DEVICE_TYPE to "" at the top, so a value inherited from the calling workflow still passes through as upstream intended, just without newlines. I did not run the action to test this.

