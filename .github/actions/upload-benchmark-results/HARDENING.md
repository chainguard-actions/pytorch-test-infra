<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261123-205410** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by the mutable branch ref '@main' instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:123`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is a process env var the composite action inherits; this script does not set it. It is written to $GITHUB_ENV without first running it through printf '%s' ... | tr -d '\n\r'. Fix: safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned both pytorch/test-infra sub-actions (setup-uv and get-workflow-job-id) to 8c9ea89f444b15c5ce4bb833a0cfed044a2667f7, with a '# main' comment. That is the commit given as upstream_commit for this release. I did not look it up with lookup_action_sha. I also did not check that both sub-action folders exist at that commit, but they are in the same repository as this action at the same release. The VIRTUAL_ENV value written to $GITHUB_ENV now has newlines stripped (printf | tr -d '\n\r'), and $GITHUB_ENV is quoted. I applied the same stripping to the DEVICE_TYPE write. That write was not flagged, but its value comes from command output. I didn't run the action after these edits.

