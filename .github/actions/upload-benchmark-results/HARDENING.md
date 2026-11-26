<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml pins two composite steps to the mutable branch ref @main instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115).

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes the inherited process env var RUNNER_TEMP to $GITHUB_ENV without sanitizing it first: 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. The script reads RUNNER_TEMP but never sets it, so under the check's composite-action rule it counts as workflow-controlled. Fix: compute safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r') and write "VIRTUAL_ENV=$safe" to "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Changed the setup-uv and get-workflow-job-id sub-actions from @main to the upstream commit bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, which this mirror version was built from. I checked the SHA with lookup_action_sha and left a '# v20261118-220128' comment so the version stays readable. The VIRTUAL_ENV value is now passed through tr -d '\n\r' to strip newlines before it is written to "$GITHUB_ENV", and $GITHUB_ENV is now quoted. I didn't run the action after the edits.

