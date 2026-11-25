<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step pins its action to a branch, not a 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited env var RUNNER_TEMP, which this script does not set. It then writes them to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without the `printf '%s' ... | tr -d '\n\r'` sanitization step first. A calling workflow could set RUNNER_TEMP to a value containing newlines and inject extra environment variables.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

1. unpinned-uses: the step used pytorch/test-infra/.github/actions/setup-nvidia@main. It now points at 13fc79c71b9a7c86a46d898782991a6418778f0b, the upstream commit this mirror version was built from. lookup_action_sha confirmed that SHA exists. A comment keeps the original ref name.

2. github-env-injection: in the 'Setup useful environment variables' step, the three directory paths (RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR, RUNNER_DOCS_DIR) now have newlines and carriage returns stripped with printf '%s' | tr -d '\n\r' before they're written to $GITHUB_ENV. The directories are still created the same way as upstream. Each value is a fixed path under RUNNER_TEMP, so a normal value comes out unchanged.

