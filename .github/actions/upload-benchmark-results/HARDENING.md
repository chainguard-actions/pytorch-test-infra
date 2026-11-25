<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs point to a branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115).

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes a value built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV with no sanitization step first: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. The script reads RUNNER_TEMP but does not set it, so this check treats it as workflow-controlled. Fix: run printf '%s' "$RUNNER_TEMP/benchmark-upload-venv" | tr -d '\n\r' first, write the result, and quote "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both pytorch/test-infra sub-action references (setup-uv, get-workflow-job-id) to 13fc79c71b9a7c86a46d898782991a6418778f0b (the upstream commit this version came from, verified with lookup_action_sha), with a '# main' comment. Install dependencies step now runs the VIRTUAL_ENV path through tr -d '\n\r' before writing it to $GITHUB_ENV, and $GITHUB_ENV is now quoted.

