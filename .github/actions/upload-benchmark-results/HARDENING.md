<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite action steps reference another action by the `main` branch instead of a full 40-character commit SHA. Whoever controls that branch can change the code these steps run. Failing lines: `uses: pytorch/test-infra/.github/actions/setup-uv@main` (line 31) and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` (line 115).

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to the upstream commit 13fc79c71b9a7c86a46d898782991a6418778f0b (the commit this action version was built from), keeping a '# main' comment.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, the 'Install dependencies' step now strips newlines and carriage returns from the VIRTUAL_ENV value (${RUNNER_TEMP}/benchmark-upload-venv) using tr -d '\n\r' before writing it to "$GITHUB_ENV", and $GITHUB_ENV is now quoted. I made the same change to the DEVICE_TYPE write in 'Get device type' because that value comes from command output. No other behaviour changed. I haven't run the action or any tests.

