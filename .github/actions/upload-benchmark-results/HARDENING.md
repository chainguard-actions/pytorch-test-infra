<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point at a mutable branch instead of a full 40-character commit SHA: (1) 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (2) 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. Anyone who can push to that branch can change the code these steps run. Pin each one to a commit SHA.

Locations:

- `action.yml:30`
- `action.yml:114`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is an inherited process env var that this run script reads but does not set, so under this check it counts as workflow-controlled. The value goes into $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' cleanup, so a value containing a newline could inject extra env lines. Clean it first, e.g. safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'); echo "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV".

Locations:

- `action.yml:40`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned both pytorch/test-infra sub-actions (setup-uv, get-workflow-job-id) to bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c, the upstream commit this version was built from (verified with lookup_action_sha). The VIRTUAL_ENV value now has newlines stripped with printf | tr -d '\n\r' before it is written to $GITHUB_ENV, which is now quoted.

