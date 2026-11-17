<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20260922-155642** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses action refs pinned to tags instead of 40-character commit SHAs: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". An attacker-controlled branch or tag name can break out of the quotes and run commands. Pass these values through env: variables and quote them.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): the 'Setup conda environment for build' step expands the env var PYTHON_VERSION (from inputs.python-version) without quotes: 'case $PYTHON_VERSION in'. It should be 'case "$PYTHON_VERSION" in'.

Locations:

- `action.yml:161`

### github-env-injection (severity: high)

The 'Set artifact name' step writes 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"'. This value comes from untrusted sources: inputs.python-version, inputs.cuda-version and inputs.arch (passed in through env), plus REPOSITORY and REF, which this step inherits from the calling environment. None of them goes through printf '%s' ... | tr -d '\n\r' first, so a newline in any of them could inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a… (v4) and conda-incubator/setup-miniconda to 505e6394… (v3.1.1). In 'Log Available Webhook Fields', moved the github.* expressions into env vars that the script now echoes. Quoted $PYTHON_VERSION in the case statement. In 'Set artifact name', the ARTIFACT_NAME value is built first and passed through printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV. REPOSITORY and REF still come from the caller's environment, as they did upstream.

