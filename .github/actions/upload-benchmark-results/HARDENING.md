<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses actions by a branch name, not a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31) and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 115). If either branch changes, this action runs the new code without review. Pin both to a full commit SHA.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step runs 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP is a process env var this composite action inherits from the caller; the same run: script does not compute it. It goes into $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' step, so a newline in the value could add extra env entries. Strip newlines first, e.g. safe=$(printf '%s' "${RUNNER_TEMP}/benchmark-upload-venv" | tr -d '\n\r'), then write "VIRTUAL_ENV=$safe" >> "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to 6f7274a0eff04dd4f8ada574e4e144610cece2c8. That is the upstream commit this mirror was built from, and I confirmed it with lookup_action_sha. I left a '# main' comment next to each pin. In the 'Install dependencies' step, the VIRTUAL_ENV path now goes through printf '%s' ... | tr -d '\n\r' before it is written to "$GITHUB_ENV", and $GITHUB_ENV is now quoted. The step still exports the same path, so behavior is unchanged.

