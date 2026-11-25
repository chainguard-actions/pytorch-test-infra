<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point at a mutable branch instead of a 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is a process env var that this script reads but does not set itself. The value goes into GITHUB_ENV without first being cleaned with printf '%s' ... | tr -d '\n\r'. Fix: set safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'), then write "VIRTUAL_ENV=$safe" to "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both sub-actions in action.yml (setup-uv and get-workflow-job-id) to e9b5b0a4c36ebfde49dec880ae77705038009471, with a '# main' comment. That is the upstream_commit this mirror version was built from, so the sub-actions now come from the same snapshot of pytorch/test-infra as the action itself. I did not run lookup_action_sha against the current tip of main. In the 'Install dependencies' step, the VIRTUAL_ENV value now has newlines and carriage returns stripped (printf '%s' ... | tr -d '\n\r') before it goes into $GITHUB_ENV, and $GITHUB_ENV is now quoted. Nothing was run or tested after the edits.

