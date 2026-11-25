<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261119-192116** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml points to an action by a branch name instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whatever is on that branch can change at any time and would run inside this action.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var ${RUNNER_TEMP}, which this script reads but does not set. It writes them to $GITHUB_ENV without first running `printf '%s' ... | tr -d '\n\r'`, e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. A composite action inherits env from the calling workflow, so a newline in that value could inject extra environment variables.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned the setup-nvidia step to pytorch/test-infra commit 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4 instead of the moving `main` branch. I checked that commit with lookup_action_sha; it is the upstream commit this mirror was built from. The three lines in the 'Setup useful environment variables' step that wrote paths built from RUNNER_TEMP to $GITHUB_ENV now remove newline and carriage-return characters first (`printf '%s' ... | tr -d '\n\r'`). A normal path contains neither, so the values written are the same as before. I haven't run the action or re-run the analysis to confirm the findings are cleared.

