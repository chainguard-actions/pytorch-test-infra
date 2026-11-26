<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses two actions by a branch name instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). Whoever controls the main branch can change the code these steps run. Pin each one to a full commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to the upstream commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4 (confirmed with lookup_action_sha; it is the commit this release was built from) with a '# main' comment.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Install dependencies' step of action.yml, RUNNER_TEMP is now cleaned with printf '%s' | tr -d '\n\r' before VIRTUAL_ENV is written to $GITHUB_ENV, and $GITHUB_ENV is now quoted. As an extra step beyond the finding, I applied the same newline stripping when DEVICE_TYPE (which comes from command output) is written to $GITHUB_ENV. Nothing else was changed.

