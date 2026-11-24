<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261123-205410** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml pins composite steps to a branch, not a commit SHA. Failing references: line 31 `uses: pytorch/test-infra/.github/actions/setup-uv@main` and line 128 `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin each one to a full 40-character commit SHA.

Locations:

- `action.yml:31`
- `action.yml:128`

### github-env-injection (severity: high)

The 'Install dependencies' step writes `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP is an inherited process env var. This script reads it but does not set it, so the check counts it as workflow-controlled. Nothing strips newlines before it goes into $GITHUB_ENV, so a value containing newlines could inject extra env vars. Fix: `safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r')`, then write `echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV"`.

Locations:

- `action.yml:42`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned both pytorch/test-infra sub-actions, setup-uv and get-workflow-job-id, to 8c9ea89f444b15c5ce4bb833a0cfed044a2667f7 instead of @main. That SHA is the upstream commit given in the request, the same commit this action was built from, so I did not look up a SHA with lookup_action_sha. The 'Install dependencies' step now strips newlines and carriage returns from the VIRTUAL_ENV value (built from RUNNER_TEMP) before writing it to $GITHUB_ENV, and $GITHUB_ENV is quoted. I made one change that wasn't in the findings: the DEVICE_TYPE value, which comes from command output, is cleaned the same way before it is written to $GITHUB_ENV. Nothing was tested; a fresh analysis pass is needed to confirm both findings are gone.

