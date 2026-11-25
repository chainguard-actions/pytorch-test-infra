<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261123-205410** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action calls another action by a branch name instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs at any time. Pin it to a commit SHA.

Locations:

- `action.yml:92`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds values from the inherited process env var RUNNER_TEMP, which this run block does not set. It writes them to $GITHUB_ENV without the `printf '%s' ... | tr -d '\n\r'` sanitization step, e.g. `RUNNER_ARTIFACT_DIR="${RUNNER_TEMP}/artifacts"` followed by `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR are written the same way. Composite actions inherit env from the calling workflow, so this check treats RUNNER_TEMP as untrusted. A value containing a newline could inject extra variables into $GITHUB_ENV.

Locations:

- `action.yml:63`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml. I haven't run the action to test it.

1. Unpinned action: the `setup-nvidia` step was calling `pytorch/test-infra/.github/actions/setup-nvidia@main`. It now points at commit 8c9ea89f444b15c5ce4bb833a0cfed044a2667f7, which is the upstream commit this version was built from. I confirmed with lookup_action_sha that the commit exists, and kept `# main` as a comment so readers can see where it came from.

2. Unsafe writes to $GITHUB_ENV: in the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR (all built from RUNNER_TEMP) now have newlines and carriage returns removed with `printf '%s' ... | tr -d '\n\r'` before they are written. The directory create and clean-up commands are unchanged.

