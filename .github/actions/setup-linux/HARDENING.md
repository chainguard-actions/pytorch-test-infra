<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step uses a branch ref instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step writes values built from the inherited process env var RUNNER_TEMP to $GITHUB_ENV without first running them through `printf '%s' ... | tr -d '\n\r'`. For example: `RUNNER_ARTIFACT_DIR="${RUNNER_TEMP}/artifacts"; echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are written the same way. This script does not set RUNNER_TEMP, so the check treats it as coming from the calling workflow.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml.

- unpinned-uses: The step that called pytorch/test-infra/.github/actions/setup-nvidia@main now points at commit f2f972bd8f3eab11aa0094897a81879653c6f141. That is the upstream commit this version was built from, so the step stays matched to this release. I confirmed with lookup_action_sha that the commit exists in pytorch/test-infra. A comment on the line notes it was main.
- github-env-injection: In the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are each run through printf '%s' ... | tr -d '\n\r' before being written to $GITHUB_ENV. The mkdir and rm steps are unchanged.

Nothing was run to test these edits.

