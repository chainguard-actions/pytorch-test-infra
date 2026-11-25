<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml points two composite steps at a branch instead of a full 40-character commit SHA: (1) `uses: pytorch/test-infra/.github/actions/setup-uv@main` (line 31); (2) `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` (line 115). A branch can change at any time, so anyone who can push to it controls what code these steps run.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4 (the upstream_commit this mirror version was built from), with a '# main' comment. I took the SHA from the request and did not look up the current tip of main, so the sub-actions now match the version this action was released with.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, the 'Install dependencies' step now strips newlines from the RUNNER_TEMP-based VIRTUAL_ENV value with printf '%s' | tr -d '\n\r' before writing it to $GITHUB_ENV, and $GITHUB_ENV is now quoted. The 'Get device type' step had the same pattern and was not flagged; it now cleans the command-derived DEVICE_TYPE the same way before writing it. Both values are always one line, so nothing changes when the action runs.

