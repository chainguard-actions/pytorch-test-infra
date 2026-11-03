<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite action steps reference a branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115).

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes a value built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without the required sanitization: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. The script reads RUNNER_TEMP but never sets it. A composite action inherits env from the calling workflow, so this value must be passed through printf '%s' "$RUNNER_TEMP" | tr -d '\n\r' before the write. The redirect target $GITHUB_ENV is also unquoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the setup-uv and get-workflow-job-id sub-actions to pytorch/test-infra@48c8ec0a3da135fd3b5024bf17b0d61b4ab1e81a (# main). Newlines are now stripped from RUNNER_TEMP before VIRTUAL_ENV is written to $GITHUB_ENV, and the redirect target is quoted. For defense in depth I also stripped newlines from DEVICE_TYPE, which comes from command output, before it is written, and quoted the $GITHUB_ENV redirects for DEVICE_NAME and DEVICE_TYPE. I left the existing set -u behavior as it was.

### Iteration 2

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to commit 48c8ec0a3da135fd3b5024bf17b0d61b4ab1e81a, with a '# main' comment after each.

