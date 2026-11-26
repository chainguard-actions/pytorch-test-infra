<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step pins a branch, not a commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP. It writes them to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without first running `printf '%s' ... | tr -d '\n\r'`. Under this check, values derived from env vars the caller can set must be sanitized before they are written to environment files.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in hardened/action/action.yml. Nothing has been run or tested.

1. unpinned-uses: the setup-nvidia step pointed at the `main` branch. It is now pinned to pytorch/test-infra@0569df511711f70601c984fe3a93dac324afc9ce, which is the upstream commit this version (v20261109-192709) was built from. I confirmed that SHA with lookup_action_sha and left a comment saying which version it came from.

2. github-env-injection: the 'Setup useful environment variables' step now strips newline and carriage-return characters from RUNNER_TEMP before using it. Each of the three directory paths (RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR, RUNNER_DOCS_DIR) is also cleaned the same way right before it is written to GITHUB_ENV. On a normal runner the paths come out exactly as before.

