<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261119-192116** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

A composite step references an action by branch name rather than a 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls the main branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var ${RUNNER_TEMP}. It then writes them to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without first running them through `printf '%s' ... | tr -d '\n\r'`. RUNNER_TEMP is not set inside this script, so under the check's rule it counts as untrusted.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

1. unpinned-uses: The step referenced pytorch/test-infra/.github/actions/setup-nvidia@main. It is now pinned to 7f4a746b35c7ac614b8dbfe3eb8a4e25fd23b3a4, the upstream commit this version (v20261119-192116) was built from, with a '# main' comment. I confirmed with lookup_action_sha that the commit exists. I used that commit instead of the current tip of main so the sub-action matches the upstream release.

2. github-env-injection: In the 'Setup useful environment variables' step, RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now have newlines and carriage returns stripped with printf '%s' ... | tr -d '\n\r' before they are written to $GITHUB_ENV. Directory creation and cleanup work as before.

Nothing was run to test these changes.

