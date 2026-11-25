<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to a branch name instead of a full 40-character commit SHA. Anyone who can push to that branch can change the code this action runs. Failing references: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to commit 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f, the upstream commit this version was built from (confirmed with lookup_action_sha). A '# main' comment marks each one. Nothing else was changed.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

I fixed the finding in action.yml, in the 'Install dependencies' step. Before the venv path is written to $GITHUB_ENV, it is now run through printf '%s' ... | tr -d '\n\r', and $GITHUB_ENV is quoted. A normal RUNNER_TEMP path has no newlines, so the value written is the same as before. Nothing else in the file was changed.

Two other steps in the same file also write to $GITHUB_ENV without stripping newlines, and I left both alone because they weren't in the finding. 'Get device name' writes DEVICE_NAME, but that is always one of a few fixed strings set in the script, so there is no risk. 'Get device type' writes DEVICE_TYPE, which comes from the output of tools like nvidia-smi or lscpu. That one is the more likely to come up in a future scan, and the same strip-newlines fix would apply.

Nothing was run or tested.

