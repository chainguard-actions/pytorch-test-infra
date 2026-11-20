<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by the mutable branch ref @main instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is a process env var that this run: script reads but does not set, and a composite action inherits its env from the calling workflow. It goes to $GITHUB_ENV without the required printf '%s' ... | tr -d '\n\r' sanitization, and $GITHUB_ENV is left unquoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both pytorch/test-infra sub-actions (setup-uv, get-workflow-job-id), which were on @main, to upstream_commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4, the same commit this mirror version was built from. I did not resolve the SHA with lookup_action_sha. In the 'Install dependencies' step, the VIRTUAL_ENV value now goes through printf '%s' | tr -d '\n\r' before it is written, and $GITHUB_ENV is quoted. I also quoted $GITHUB_ENV in the DEVICE_NAME and DEVICE_TYPE writes and stripped newlines from DEVICE_TYPE, which comes from command output. These were not in the findings. No other behavior changed. I made no tests or runs.

