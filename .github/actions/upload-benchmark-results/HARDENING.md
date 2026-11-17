<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20260922-155642** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that use mutable branch refs where a commit SHA should be: `uses: pytorch/test-infra/.github/actions/setup-uv@main` (line 31) and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` (line 115). Pin both to a full 40-character commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to commit 28dee7456d0348d74a5faa85098bb028b263ee2b (the upstream commit this mirror was built from, verified via lookup), keeping '# main' comments.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Install dependencies' step of action.yml, the venv path is now built in a local variable and cleaned with printf '%s' | tr -d '\n\r' before it is exported and written to "$GITHUB_ENV" (now quoted). I made the same change in the 'Get device type' step, where DEVICE_TYPE was also written to GITHUB_ENV without being cleaned. That location wasn't in the findings. It still reads plain "$DEVICE_TYPE", so under set -u the step fails the same way upstream does if the variable is unset.

