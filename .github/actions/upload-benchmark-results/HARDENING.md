<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by the mutable branch ref '@main' rather than a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 112). Whoever controls the main branch of pytorch/test-infra can change what code runs in this action.

Locations:

- `action.yml:31`
- `action.yml:112`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Both '@main' references in action.yml are now pinned to a full commit SHA, with '# main' kept as a comment: pytorch/test-infra/.github/actions/setup-uv and pytorch/test-infra/.github/actions/get-workflow-job-id. The SHA is 9206d491d3a5507163cb9d5b77040d4c3ef5e038, the upstream test-infra commit this mirror version was built from (upstream_commit). That way the sub-actions match the version of the action that calls them, not whatever main points to today. I didn't run the action and didn't check that both sub-action folders exist at that commit; I'm assuming they do because the calling action came from the same commit.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, the 'Install dependencies' step was writing ${RUNNER_TEMP}/benchmark-upload-venv straight into $GITHUB_ENV. It now strips newlines and carriage returns first (printf '%s' ... | tr -d '\n\r') and quotes "$GITHUB_ENV". The path written is the same as before, so behaviour doesn't change. Nothing was run or tested. Not changed: the later steps that write DEVICE_NAME and DEVICE_TYPE to $GITHUB_ENV also don't strip newlines, but they weren't in the finding. DEVICE_TYPE comes from hardware tool output (nvidia-smi, lscpu and similar), not from the calling workflow.

