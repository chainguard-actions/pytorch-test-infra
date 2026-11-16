<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261021-234439** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose `uses:` refs point at a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:31`
- `action.yml:114`

### github-env-injection (severity: high)

The 'Install dependencies' step writes `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP comes from the process environment this composite action inherits. The script reads it but never sets it, and newlines are not stripped with `printf '%s' ... | tr -d '\n\r'` before the write. Under this check's rules, inherited env vars count as workflow-controlled.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both pytorch/test-infra sub-actions (setup-uv and get-workflow-job-id) to 4bb924e6cddf98370d0c754d6769b492fe457233, the upstream commit this mirror was built from, with a '# main' comment. The VIRTUAL_ENV value written to $GITHUB_ENV now has newlines stripped first (printf '%s' ... | tr -d '\n\r'), and $GITHUB_ENV is quoted. I gave the DEVICE_TYPE write the same treatment as a precaution, since that value comes from command output. Nothing else changed, and set -u still behaves as before.

