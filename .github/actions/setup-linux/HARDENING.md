<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step pins its action to a branch, not a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var RUNNER_TEMP. It then writes them to $GITHUB_ENV (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`) without first running `printf '%s' ... | tr -d '\n\r'`. RUNNER_TEMP is not set inside the script, and a composite action inherits env from the calling workflow. A value containing newlines could therefore add extra environment variables.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in hardened/action/action.yml. I haven't run the action since the changes.

1. **unpinned-uses:** The step that installs the NVIDIA driver used `pytorch/test-infra/.github/actions/setup-nvidia@main`. I pinned it to `0569df511711f70601c984fe3a93dac324afc9ce`, the upstream commit this mirror was built from. That keeps setup-nvidia on the same code as the rest of this release. I didn't look up the current head of `main`, so the pin is to that build commit, not to whatever `main` points at today.

2. **github-env-injection:** In the 'Setup useful environment variables' step, `RUNNER_TEMP` now has newlines and carriage returns stripped once at the top. Each of the three values (RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR, RUNNER_DOCS_DIR) is also cleaned with `printf '%s' | tr -d '\n\r'` right before it is written to $GITHUB_ENV. For a normal `RUNNER_TEMP` the directories and the values written are the same as before.

