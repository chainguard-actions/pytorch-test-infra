<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-232755** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin both to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:117`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to the upstream commit 2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f (the commit this mirror version was built from), keeping a '# main' comment.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Fixed the flagged write in the 'Install dependencies' step of action.yml. The path built from RUNNER_TEMP now has newlines removed with printf '%s' ... | tr -d '\n\r' before it goes into "$GITHUB_ENV". I also applied the same newline removal to the DEVICE_TYPE write in 'Get device type' as a precaution; that one wasn't flagged. Nothing else in the action changed, and I didn't run the action to test either edit.

