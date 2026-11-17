<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261109-192709** was hardened automatically. 1 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by the mutable branch ref @main instead of a full 40-character commit SHA: (1) 'uses: pytorch/test-infra/.github/actions/setup-uv@main' (line 31); (2) 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main' (line 117). Pin each one to a commit SHA.

Locations:

- `action.yml:31`
- `action.yml:117`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-uv and get-workflow-job-id from @main to 0569df511711f70601c984fe3a93dac324afc9ce, the upstream commit this mirror version was built from (checked with lookup_action_sha). The sub-actions now run at the same commit as the action itself.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In the 'Install dependencies' step of action.yml, the VIRTUAL_ENV path built from RUNNER_TEMP now has newlines and carriage returns removed (printf '%s' ... | tr -d '\n\r') before it is written to $GITHUB_ENV. The $GITHUB_ENV reference is now quoted too. I haven't run the action to test the change.

