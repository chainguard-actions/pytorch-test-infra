<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261119-192116** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point `uses:` at a mutable branch ref instead of a full 40-character commit SHA: (1) `uses: pytorch/test-infra/.github/actions/setup-uv@main` and (2) `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin each one to a commit SHA, with the version in a trailing comment.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

In the 'Install dependencies' composite step, a value built from the inherited process env var RUNNER_TEMP is written to $GITHUB_ENV with no sanitization: `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP is read from the caller's environment, not set in this script, so this check counts it as workflow-controlled. Strip newlines before the write, e.g. `safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV"`.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the two pytorch/test-infra sub-actions (setup-uv and get-workflow-job-id) to 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4, with '# main' as a trailing comment. That commit is the upstream commit this mirror version was built from, so it matches the code that was published. Before writing VIRTUAL_ENV to $GITHUB_ENV, the path built from RUNNER_TEMP now has newlines stripped, and $GITHUB_ENV is quoted. Nothing was run to test these changes.

