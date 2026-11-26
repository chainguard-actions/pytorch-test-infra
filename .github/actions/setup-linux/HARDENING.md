<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step refers to an action by branch instead of by a full commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:91`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP, then writes them to $GITHUB_ENV with no sanitization (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`). The script reads RUNNER_TEMP but does not set it, and composite actions inherit env from the calling workflow, so the check treats it as untrusted. Strip newlines first with `printf '%s' ... | tr -d '\n\r'` before each write.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned pytorch/test-infra/.github/actions/setup-nvidia from @main to f2f972bd8f3eab11aa0094897a81879653c6f141, the upstream commit this mirror version was built from. lookup_action_sha confirmed the SHA exists in pytorch/test-infra. The pinned code is what upstream's main pointed to when this release was cut, not today's main. In 'Setup useful environment variables', RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now have newlines stripped (printf '%s' | tr -d '\n\r') before each one is written to GITHUB_ENV. The directory handling (rm -rf, mkdir) is the same as upstream. Nothing was run or tested after these edits.

