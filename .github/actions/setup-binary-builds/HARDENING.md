<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261109-192709** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses action refs pinned to a tag, not a full commit SHA: 'uses: actions/checkout@v4' and 'uses: conda-incubator/setup-miniconda@v3.1.1'.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into its run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". The ref values can be chosen by an attacker (branch or tag names), so they could inject shell commands.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, the env var PYTHON_VERSION comes from inputs.python-version and is expanded without quotes in 'case $PYTHON_VERSION in'. It should be written as 'case "$PYTHON_VERSION" in'. The shellcheck SC2153 directive does not cover this case.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"' with no sanitization. CU_VERSION and ARCH come from inputs, SHORT_PYTHON_VERSION is derived from inputs.python-version, and REPOSITORY and REF are env vars inherited from the calling workflow. None of these pass through printf '%s' ... | tr -d '\n\r' first, so a newline in any of them could inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a… (v4) and setup-miniconda to 505e6394… (v3.1.1). Moved github.ref_name, event.ref, ref and base_ref into env vars in the logging step. Quoted $PYTHON_VERSION in the case statement. In 'Set artifact name' the ARTIFACT_NAME value is now built first, then passed through printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV.

