<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261109-232755** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references actions by mutable tags instead of 40-char commit SHAs: 'uses: actions/checkout@v4' and 'uses: conda-incubator/setup-miniconda@v3.1.1'.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): step 'Log Available Webhook Fields' puts GitHub expressions straight into the run script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". Ref names can be controlled by an attacker. Pass them in through env: and quote them, or use the existing $GITHUB_REF_NAME/$GITHUB_REF/$GITHUB_BASE_REF variables.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): step 'Setup conda environment for build' expands the input-derived env var PYTHON_VERSION (from inputs.python-version) without quotes in a case statement: 'case $PYTHON_VERSION in'. It should be 'case "$PYTHON_VERSION" in'.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

Step 'Set artifact name' writes values built from untrusted inputs to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization step. The values are SHORT_PYTHON_VERSION (from inputs.python-version), CU_VERSION (inputs.cuda-version), ARCH (inputs.arch), and the inherited env vars REPOSITORY and REF. The offending line is: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A newline in any of these values lets the caller inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

I fixed all four findings in action.yml.

- **unpinned-uses:** actions/checkout is now pinned to commit 11d5960a326750d5838078e36cf38b85af677262 (v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). The SHAs came from lookup_action_sha.
- **script-injection (webhook log step):** the four github.* expressions now go through the step's env: block (GH_REF_NAME, GH_EVENT_REF, GH_REF, GH_BASE_REF) and are echoed as quoted shell variables. The step prints the same values as before.
- **script-injection (case statement):** `case $PYTHON_VERSION in` is now `case "$PYTHON_VERSION" in`.
- **github-env-injection:** the artifact name is built into a variable first, newlines are stripped with `printf '%s' ... | tr -d '\n\r'`, and only then is it written to GITHUB_ENV. The name itself is built exactly as before.

Nothing was run or tested.

