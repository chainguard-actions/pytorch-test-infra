<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261109-232755** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references actions by mutable tags instead of 40-character commit SHAs: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 91).

Locations:

- `action.yml:55`
- `action.yml:91`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". Ref and branch names can be controlled by an attacker. Because these values are substituted into the script text before the shell runs, a crafted name can run commands.

Locations:

- `action.yml:70`

### script-injection (severity: high)

Rule (b): the 'Setup conda environment for build' step expands PYTHON_VERSION (from inputs.python-version) without quotes: 'case $PYTHON_VERSION in'. The shellcheck directive above it disables only SC2153, not SC2086 or SC2206, and this is not an array assignment, so the exception does not apply. It should be 'case "$PYTHON_VERSION" in'.

Locations:

- `action.yml:151`

### github-env-injection (severity: high)

The 'Set artifact name' step writes 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"' with no printf '%s' ... | tr -d '\n\r' step first. CU_VERSION and ARCH come from inputs, and SHORT_PYTHON_VERSION comes from inputs.python-version. The sed call does not remove newlines when the pattern doesn't match. REPOSITORY and REF are not set in this step, so they are inherited from the calling workflow's environment. Any of these values can carry newlines that inject extra environment variables.

Locations:

- `action.yml:88`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout (v4 -> 11d5960a...) and conda-incubator/setup-miniconda (v3.1.1 -> 505e6394...). Moved the github.ref_name, event.ref, ref and base_ref expressions in 'Log Available Webhook Fields' into env vars. Put quotes around $PYTHON_VERSION in the case statement. ARTIFACT_NAME now has newlines and carriage returns stripped with printf | tr -d '\n\r' before it is written to GITHUB_ENV. REPOSITORY and REF still come from the calling workflow's environment, as they do upstream.

