<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to a branch instead of a full 40-character commit SHA, so whatever lands on that branch upstream runs inside this action: `uses: pytorch/test-infra/.github/actions/setup-uv@main` (line 31) and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` (line 113). Pin both to a full commit SHA.

Locations:

- `action.yml:31`
- `action.yml:113`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned the two pytorch/test-infra composite steps in action.yml (setup-uv on line 31 and get-workflow-job-id on line 113) to commit 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f, keeping a '# main' comment. I chose this commit rather than the current tip of main because it is the upstream commit this mirror version was built from, so the sub-actions match the rest of the action's code. lookup_action_sha returned the same SHA. Nothing else was changed.

