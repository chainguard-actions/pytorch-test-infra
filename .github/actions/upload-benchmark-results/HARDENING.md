<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs point at a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-uv@main` and `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:31`
- `action.yml:115`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned two `uses:` references in action.yml to the full commit bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, with a `# main` comment: pytorch/test-infra/.github/actions/setup-uv@main and pytorch/test-infra/.github/actions/get-workflow-job-id@main. That commit is the upstream_commit from the request, the one this action version was built from. I took the SHA from the request rather than resolving `main` now, so the sub-actions stay in step with the rest of the action's code. No other changes were made.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, the 'Install dependencies' step now strips newlines from the VIRTUAL_ENV value (${RUNNER_TEMP}/benchmark-upload-venv) with tr -d '\n\r' before writing it to "$GITHUB_ENV". Also stripped newlines from DEVICE_TYPE, which comes from command output, before it is written to GITHUB_ENV. Nothing else changed.

