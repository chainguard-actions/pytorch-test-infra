<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261123-205410** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs point at a mutable branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 121). Pin both to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:121`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Both sub-action refs in action.yml were on the moving `main` branch. I pinned them to commit 8c9ea89f444b15c5ce4bb833a0cfed044a2667f7 and kept `# main` as a trailing comment:
- `pytorch/test-infra/.github/actions/setup-uv` (line 31)
- `pytorch/test-infra/.github/actions/get-workflow-job-id` (line 121)

This is the upstream commit this mirror version (v20261123-205410) was built from, so the sub-actions now come from the same snapshot of the repo as the action itself. Before using it I checked with lookup_action_sha that the commit exists in pytorch/test-infra. These were the only two `uses:` references in action.yml. I haven't run the action since the change.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

I fixed the github-env-injection finding in the 'Install dependencies' step of action.yml. The VIRTUAL_ENV value is now cleaned with printf '%s' ... | tr -d '\n\r' before it goes into $GITHUB_ENV, and $GITHUB_ENV is quoted. I also made the same kind of fix in the 'Get device type' step, where DEVICE_TYPE (taken from device-tool output) now has newlines stripped before it is written. In the 'Get device name' step I only quoted $GITHUB_ENV, because DEVICE_NAME is always a fixed literal. Nothing else changed, and I did not run the action to check these edits.

