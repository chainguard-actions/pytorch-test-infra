<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20260922-155642** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite steps pull in actions by a branch name instead of a full 40-character commit SHA: line 31 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and line 115 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. Pin both to a commit SHA, with the version as a comment.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP comes from the process environment this composite action inherits; the script does not set it. The check requires such values to go through printf '%s' "$RUNNER_TEMP" | tr -d '\n\r' before being written to $GITHUB_ENV, and that step is missing. In practice the runner sets RUNNER_TEMP, so the real risk is low, but under the check's rule it counts as a failure. Fix: strip newlines from the value first, e.g. safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml.

- unpinned-uses: The setup-uv and get-workflow-job-id steps now point to commit 28dee7456d0348d74a5faa85098bb028b263ee2b, with '# main' as a comment. That is the upstream commit this mirror version was built from (upstream_commit in the request). Upstream main has since moved to c91174703a487849783425932bef8cdf24e3154c. I used the build commit so the two sub-actions match the code this version shipped with.

- github-env-injection: The 'Install dependencies' step now removes newlines from the VIRTUAL_ENV value with printf '%s' | tr -d '\n\r' before writing it to $GITHUB_ENV.

Two changes beyond the findings: DEVICE_TYPE comes from command output (nvidia-smi, lscpu and others), so I also remove newlines from it before writing it to $GITHUB_ENV. I also put quotes around $GITHUB_ENV in the DEVICE_NAME and DEVICE_TYPE writes. Nothing was run to test these changes.

