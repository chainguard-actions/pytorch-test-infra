<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps reference actions by the mutable branch '@main' instead of a full 40-character commit SHA: line 31 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and line 115 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is an inherited process env var: this run: script reads it but never sets it. The value goes into $GITHUB_ENV without the required sanitization step (printf '%s' ... | tr -d '\n\r'). Fix: safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both pytorch/test-infra sub-actions (setup-uv and get-workflow-job-id) to 0569df511711f70601c984fe3a93dac324afc9ce, the upstream commit this version was built from (lookup_action_sha confirmed it), with a '# main' comment. The VIRTUAL_ENV value is now stripped of newlines before it is written to $GITHUB_ENV, and $GITHUB_ENV is quoted. I made the same change to the DEVICE_TYPE write, which the findings did not list. DEVICE_TYPE comes from command output, so it could contain a newline.

