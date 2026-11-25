<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by a branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). Anyone who can push to that branch changes the code this action runs.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes the inherited process env var RUNNER_TEMP to $GITHUB_ENV without sanitising it first: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. The script reads RUNNER_TEMP but never sets it, so in a composite action it counts as workflow-controlled. The value needs 'printf '%s' ... | tr -d '\n\r'' immediately before the write.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra setup-uv and get-workflow-job-id to commit f2f972bd8f3eab11aa0094897a81879653c6f141. That is the upstream commit this version was built from, and I confirmed it exists with lookup_action_sha. Each pin keeps a '# main' comment. In 'Install dependencies', the VIRTUAL_ENV value is now passed through printf '%s' ... | tr -d '\n\r' right before it is written to $GITHUB_ENV, and $GITHUB_ENV is now quoted. The venv path itself is the same as before.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Fixed the 'Get device type' step in action.yml. The script now sets DEVICE_TYPE to empty at the start, so a value passed in by the calling workflow can't carry through. Newlines and carriage returns are stripped with printf '%s' "${DEVICE_TYPE:-}" | tr -d '\n\r' before the value goes into "$GITHUB_ENV". Also quoted $GITHUB_ENV on the DEVICE_NAME write in the step before it; that value is always one of the fixed device names. Nothing has been run or tested.

One behaviour change: if a calling workflow overrides DEVICE_NAME with something other than the six known names, DEVICE_TYPE is now written as empty instead of keeping the caller's value. Normally the previous step always sets DEVICE_NAME to one of those six, so this shouldn't come up.

