<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite action steps reference actions by the mutable branch ref '@main' instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to the upstream commit 9206d491d3a5507163cb9d5b77040d4c3ef5e038, the test-infra commit this action version was built from, keeping a '# main' comment for readability. I took that SHA from the request's upstream_commit and did not resolve it with lookup_action_sha. It belongs to the same repository as this action, so the sub-actions now match the action's own version instead of whatever main points to now. No other changes.

