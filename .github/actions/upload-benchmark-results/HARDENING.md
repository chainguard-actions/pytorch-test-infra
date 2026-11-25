<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps reference actions by a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:31`
- `action.yml:114`

### github-env-injection (severity: high)

The 'Install dependencies' step writes `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP is an inherited process env var that this script reads but does not set, so the composite-action rule (e) treats it as workflow-controlled. The value is not passed through `printf '%s' ... | tr -d '\n\r'` before the write, and $GITHUB_ENV is not quoted.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both sub-actions to the full SHA of commit bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, with a '# main' comment. That commit is the upstream commit this version was built from, and lookup_action_sha confirmed it exists, so the sub-actions now match the code this release shipped with. The VIRTUAL_ENV value is now passed through printf '%s' | tr -d '\n\r' before it is written to "$GITHUB_ENV", and that variable is now quoted. Separately, I also quoted $GITHUB_ENV in the DEVICE_NAME and DEVICE_TYPE writes, which the findings didn't flag. No test was run.

