<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action step pulls in a remote action by a branch name instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs at any time. Pin it to a commit SHA.

Locations:

- `action.yml:90`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds three values from the inherited process env var RUNNER_TEMP (for example `RUNNER_ARTIFACT_DIR="${RUNNER_TEMP}/artifacts"`) and writes them to $GITHUB_ENV (`echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`, and the same for RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR). The step does not first run the values through `printf '%s' ... | tr -d '\n\r'`. Under this check, any env var a composite action inherits rather than computes counts as workflow-controlled. In practice the runner normally sets RUNNER_TEMP, so the real risk is lower than the rating suggests.

Locations:

- `action.yml:66`
- `action.yml:71`
- `action.yml:76`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned `pytorch/test-infra/.github/actions/setup-nvidia@main` to `@2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f # main`. This is the upstream commit the mirror was built from, so setup-nvidia now comes from the same version as this action. The current main was 8cd319865066bf94e5be2b0180d081175095c980 at lookup time. In 'Setup useful environment variables', each of RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now has newlines stripped (printf '%s' | tr -d '\n\r') before it is written to $GITHUB_ENV. The stripping is done outside any other command and printf can't fail, so no errors get hidden.

