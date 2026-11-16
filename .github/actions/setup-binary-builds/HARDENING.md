<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261021-234439** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses actions by mutable tag instead of a full 40-character commit SHA: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". Ref names can be controlled by an attacker, and these values are substituted into the script before bash runs it. Use the GITHUB_REF_NAME, GITHUB_REF and GITHUB_BASE_REF env vars instead, quoted (the same step already echoes them).

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): the 'Setup conda environment for build' step expands the env var PYTHON_VERSION without quotes. It comes from ${{ inputs.python-version }}. Offending line: 'case $PYTHON_VERSION in'. Quote it: 'case "$PYTHON_VERSION" in'. The '# shellcheck disable=SC2153' directive above it does not exempt it, because the exemption only covers array assignments with SC2086/SC2206.

Locations:

- `action.yml:161`

### github-env-injection (severity: high)

The 'Set artifact name' step writes workflow-controlled values to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization step: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". CU_VERSION and ARCH come from inputs.cuda-version and inputs.arch. REPOSITORY and REF are inherited process env vars that this step does not set. A newline in any of them can inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). Moved github.ref_name/event.ref/ref/base_ref expressions in the 'Log Available Webhook Fields' step into env vars and echo them quoted. Quoted the case subject (case "$PYTHON_VERSION" in). The ARTIFACT_NAME value is now passed through printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV.

