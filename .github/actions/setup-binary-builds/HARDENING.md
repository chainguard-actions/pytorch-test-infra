<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261125-022556** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs are tags, not full commit SHAs: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}" and echo "${{ github.base_ref }}". Branch and ref names can be controlled by an attacker. The fix is to pass these through env: variables, or use the GITHUB_REF_NAME, GITHUB_REF and GITHUB_BASE_REF variables the script already echoes above.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, PYTHON_VERSION comes from inputs.python-version and is expanded without quotes in 'case $PYTHON_VERSION in'. The '# shellcheck disable=SC2153' directive does not qualify for the array-assignment exception. It should be quoted: case "$PYTHON_VERSION" in.

Locations:

- `action.yml:154`

### github-env-injection (severity: high)

The 'Set artifact name' step writes workflow-controlled values to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". CU_VERSION and ARCH come from inputs.*. SHORT_PYTHON_VERSION comes from inputs.python-version through sed, which works line by line and keeps any later lines of a multi-line value. REPOSITORY and REF are inherited process env vars that this step does not set. A newline in any of them could inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout (v4) and conda-incubator/setup-miniconda (v3.1.1) to their full commit SHAs, keeping the tag name in a comment. In the 'Log Available Webhook Fields' step, the github.ref_name, github.event.ref, github.ref and github.base_ref expressions now go through env: variables. Quoted $PYTHON_VERSION in the case statement. In 'Set artifact name', the ARTIFACT_NAME value is now built first and has newlines stripped with printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV. Nothing was run or tested; these are text edits to action.yml only.

