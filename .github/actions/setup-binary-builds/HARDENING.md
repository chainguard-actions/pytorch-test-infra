<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs are tags, not commit SHAs: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92). Pin each one to a full 40-character commit SHA.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". A branch or ref name can contain shell metacharacters, and they run when the script runs. Use the env vars that are already available instead ($GITHUB_REF_NAME, $GITHUB_REF, $GITHUB_BASE_REF), or pass the values through env: and quote them.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, PYTHON_VERSION comes from inputs.python-version and is expanded without quotes in a case statement: 'case $PYTHON_VERSION in'. Quote it: case "$PYTHON_VERSION" in.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"' with no sanitization. REPOSITORY and REF are never set in this step, so their values come from the calling workflow's env. CU_VERSION and ARCH come from inputs, and SHORT_PYTHON_VERSION comes from inputs.python-version. A newline in any of these values could add extra variables to GITHUB_ENV. Pass each value through printf '%s' ... | tr -d '\n\r' before the write.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to the commit for v4 (11d5960a…) and conda-incubator/setup-miniconda to the commit for v3.1.1 (505e6394…), keeping the tag names as comments. In the 'Log Available Webhook Fields' step, the github.ref_name, github.event.ref, github.ref and github.base_ref expressions now come in through env: and are echoed as quoted variables. I put $PYTHON_VERSION in quotes in the case statement. ARTIFACT_NAME is now built in a variable first and run through printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV. Nothing was tested; these are edits to action.yml only.

