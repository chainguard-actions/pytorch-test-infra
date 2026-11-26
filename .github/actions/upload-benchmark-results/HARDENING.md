<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to a mutable branch instead of a 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). Pin both to a full commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step runs 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is an inherited process env var that this script reads but does not set, and it is written to $GITHUB_ENV without the required sanitization (printf '%s' ... | tr -d '\n\r'). The runner normally sets RUNNER_TEMP, so the risk is low in practice, but the check requires sanitizing any inherited value. Fix: safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml. Nothing was run or tested after the edits.

- unpinned-uses: The two pytorch/test-infra steps (setup-uv and get-workflow-job-id) were on @main. They are now pinned to upstream_commit 13fc79c71b9a7c86a46d898782991a6418778f0b with a '# v20261125-022556' comment. That is the commit this version came from, so the steps it calls match the rest of the action. I took it from the request and did not resolve it with lookup_action_sha.
- github-env-injection: In the 'Install dependencies' step, the VIRTUAL_ENV value is now passed through printf '%s' | tr -d '\n\r' before it goes to "$GITHUB_ENV".
- Not in the findings: the 'Get device type' step writes DEVICE_TYPE, which comes from hardware tool output, to GITHUB_ENV. I strip newlines from it the same way.

