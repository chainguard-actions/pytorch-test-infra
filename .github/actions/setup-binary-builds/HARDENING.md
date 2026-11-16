<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261109-192709** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml pins composite steps to tags instead of full commit SHAs: 'uses: actions/checkout@v4' and 'uses: conda-incubator/setup-miniconda@v3.1.1'.

Locations:

- `action.yml:55`
- `action.yml:90`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". A crafted ref or branch name could inject shell commands. Read them from env vars like $GITHUB_REF_NAME instead.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): the 'Setup conda environment for build' step expands a value from inputs.python-version without quotes: 'case $PYTHON_VERSION in'. It should be 'case "$PYTHON_VERSION" in'.

Locations:

- `action.yml:145`

### github-env-injection (severity: high)

The 'Set artifact name' step writes 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"' with no sanitization. CU_VERSION and ARCH come from inputs, SHORT_PYTHON_VERSION comes from inputs.python-version, and REPOSITORY/REF are env vars inherited from the calling workflow. None of them pass through printf '%s' ... | tr -d '\n\r' first, so a value containing a newline can inject arbitrary environment variables.

Locations:

- `action.yml:87`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

All four findings are fixed in action.yml.

- **unpinned-uses:** pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). The SHAs came from lookup_action_sha, and each line keeps its tag as a trailing comment.
- **script-injection (Log Available Webhook Fields step):** the four expressions (github.ref_name, github.event.ref, github.ref, github.base_ref) now come in through the step's env: block as GH_CTX_* variables, and the script echoes those quoted variables. The step still logs the same values.
- **script-injection (Setup conda environment for build step):** `case $PYTHON_VERSION in` is now `case "$PYTHON_VERSION" in`.
- **github-env-injection (Set artifact name step):** the artifact name is built the same way as before, passed through `printf '%s' ... | tr -d '\n\r'`, and then written to GITHUB_ENV, so a newline in any part of it can no longer add extra environment variables. The step uses `set -euxo pipefail`, so a failing command still stops it.

