<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references actions by mutable tag instead of a full 40-char commit SHA: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): step 'Log Available Webhook Fields' puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". Values such as branch or tag names can contain shell metacharacters. Pass them through env: and quote them, or use the existing $GITHUB_REF_NAME / $GITHUB_REF / $GITHUB_BASE_REF variables.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): step 'Setup conda environment for build' expands an input-derived env var without quotes: 'case $PYTHON_VERSION in'. PYTHON_VERSION comes from inputs.python-version. Quote it as case "$PYTHON_VERSION" in.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

Step 'Set artifact name' writes untrusted values to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". CU_VERSION and ARCH come from inputs, and SHORT_PYTHON_VERSION comes from inputs.python-version. REPOSITORY and REF are not set in this step, so they are inherited from the calling workflow. Any of them could carry a newline that injects more environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). Moved the github.ref_name, event.ref, ref and base_ref expressions in 'Log Available Webhook Fields' into env vars. Quoted the case "$PYTHON_VERSION" in the conda setup step. ARTIFACT_NAME now has newlines stripped (printf '%s' | tr -d '\n\r') before it is written to GITHUB_ENV.

