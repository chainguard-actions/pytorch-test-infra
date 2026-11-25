<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point at a mutable branch ref instead of a full 40-character commit SHA: line 31 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and line 115 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step runs 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is inherited from the process environment, not set in this run: script, and it goes into $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization step. The runner normally sets RUNNER_TEMP, so the real risk is low, but the check counts any inherited env var as untrusted. Fix: compute the value, sanitize it (safe=$(printf '%s' "$VIRTUAL_ENV" | tr -d '\n\r')), then write it to "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra setup-uv and get-workflow-job-id to the upstream commit bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, the commit this action version was built from, which keeps the sub-actions in step with the scripts used here. The VIRTUAL_ENV value now has newlines stripped (printf | tr -d '\n\r') before it is written to the quoted "$GITHUB_ENV". Not tested by running the action. The DEVICE_NAME and DEVICE_TYPE writes to $GITHUB_ENV were not flagged and still go in unsanitized; DEVICE_TYPE comes from command output, so it could get the same newline stripping if a later check flags it.

