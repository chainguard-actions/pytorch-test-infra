<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps use mutable branch refs instead of full 40-char commit SHAs: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:118`

### github-env-injection (severity: high)

'Install dependencies' step writes a value derived from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without sanitization: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is read, not computed, in this run block, so the check treats it as workflow-controlled. Clean it first with printf '%s' "$RUNNER_TEMP" | tr -d '\n\r', then write the result to "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id to commit 0569df511711f70601c984fe3a93dac324afc9ce. I took this SHA from the request's upstream_commit, which is the test-infra commit this action version was built from. I did not look it up with lookup_action_sha, and it is not the current tip of main. In the 'Install dependencies' step, RUNNER_TEMP now has newlines and carriage returns stripped (printf | tr -d '\n\r') before the VIRTUAL_ENV line is written to $GITHUB_ENV, and $GITHUB_ENV is now quoted. Separately, the steps that run Python scripts point to them with $GITHUB_ACTION_PATH/../../scripts. That only works if the mirror keeps the same folder layout as test-infra. I didn't change those paths.

