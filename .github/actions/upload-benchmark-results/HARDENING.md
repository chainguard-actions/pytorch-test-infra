<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by a branch name instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). Pin both to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

In the 'Install dependencies' step, the script writes the inherited process env var RUNNER_TEMP to $GITHUB_ENV without sanitizing it first: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is read from the environment, not set by this script, and in a composite action the environment comes from the calling workflow. Strip newlines first with printf '%s' ... | tr -d '\n\r', and quote "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the two pytorch/test-infra sub-actions (setup-uv and get-workflow-job-id) to 9206d491d3a5507163cb9d5b77040d4c3ef5e038 and kept '# main' as a comment. That SHA is the upstream commit this mirror version was built from, so the sub-actions match the code being hardened. The VIRTUAL_ENV value written to $GITHUB_ENV now has newlines and carriage returns stripped first, and $GITHUB_ENV is now quoted. Nothing was run to test these changes.

