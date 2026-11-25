<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` (line 31) and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main` (line 115). The second step receives the github-token input. Fix: pin both to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP is an env var this composite action inherits and does not set itself, and it goes into $GITHUB_ENV without the required `printf '%s' ... | tr -d '\n\r'` step. Normally the runner sets this value, so the real risk is low, but the check's rule (e) still fails it. Fix: strip newlines first, e.g. `safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV"`.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned setup-uv and get-workflow-job-id to the upstream commit 13fc79c71b9a7c86a46d898782991a6418778f0b (the commit this version was built from, confirmed via lookup_action_sha). Removed newlines from the VIRTUAL_ENV value before writing it to $GITHUB_ENV, and quoted "$GITHUB_ENV".

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Fixed in action.yml. The 'Get device type' step now strips newlines and carriage returns from DEVICE_TYPE before writing it to $GITHUB_ENV, using printf '%s' piped to tr -d '\n\r'. $GITHUB_ENV is now quoted. As an extra precaution, I applied the same fix to DEVICE_NAME in the 'Get device name' step, even though only literal values are written there. Behaviour should be unchanged: the step still runs with set -eux, so if no branch sets DEVICE_TYPE and the job doesn't already have it, the step still stops on the unset variable as before. Nothing was run to test this.

