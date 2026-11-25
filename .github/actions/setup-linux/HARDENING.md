<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite action step points to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs. Fix: pin it to a commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from RUNNER_TEMP and writes them to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`). RUNNER_TEMP is inherited from the process environment, not set by this script. The check counts that as untrusted, though in practice the runner sets RUNNER_TEMP, so the real risk is low. The values are not passed through `printf '%s' ... | tr -d '\n\r'` before the write. Fix: strip newlines from each value before writing it.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia to 6f7274a0eff04dd4f8ada574e4e144610cece2c8 (# main), the upstream_commit from the request, so the sub-action comes from the same test-infra commit this version was built from. I didn't use lookup_action_sha, because the current head of main may differ from that commit. In 'Setup useful environment variables', each of RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now has newlines stripped (printf '%s' | tr -d '\n\r') before it is written to $GITHUB_ENV. The values written are unchanged. Nothing has been run to test these changes.

