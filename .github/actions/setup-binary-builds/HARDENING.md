<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20260922-155642** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has uses: references pinned to tags instead of 40-character commit SHAs: 'uses: actions/checkout@v4' and 'uses: conda-incubator/setup-miniconda@v3.1.1'.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". Branch and ref names can be set by an attacker, so these values are substituted into the script before the shell runs it. Pass them through env: variables, or use the existing $GITHUB_REF_NAME/$GITHUB_REF/$GITHUB_BASE_REF variables, and quote them.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, the input-derived PYTHON_VERSION (from inputs.python-version) is expanded without quotes: 'case $PYTHON_VERSION in'. The shellcheck directive above it disables SC2153, not SC2086/SC2206, and this is not an array assignment. Change it to 'case "$PYTHON_VERSION" in'.

Locations:

- `action.yml:161`

### github-env-injection (severity: high)

The 'Set artifact name' step writes values the calling workflow controls into $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' cleanup step: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". CU_VERSION and ARCH come from inputs, and SHORT_PYTHON_VERSION comes from inputs.python-version. REPOSITORY and REF are not set in this step, so they are env vars inherited from the calling workflow. A newline in any of them can inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout (v4) and conda-incubator/setup-miniconda (v3.1.1) to full commit SHAs. Moved the github.ref_name, event.ref, ref and base_ref expressions in the 'Log Available Webhook Fields' step into env vars. Quoted $PYTHON_VERSION in the case statement. ARTIFACT_NAME is now built in a variable first, newlines and carriage returns are stripped with printf | tr -d '\n\r', and then it is written to GITHUB_ENV. REPOSITORY and REF are still read from the calling workflow's env, as upstream does.

