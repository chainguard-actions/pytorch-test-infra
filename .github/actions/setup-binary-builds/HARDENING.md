<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261119-192116** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has `uses:` references pinned to tags instead of full commit SHAs: `uses: actions/checkout@v4` and `uses: conda-incubator/setup-miniconda@v3.1.1`.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions directly into the run: script: `echo "${{ github.ref_name }}"`, `echo "${{ github.event.ref }}"`, `echo "${{ github.ref }}"`, `echo "${{ github.base_ref }}"`. Branch and ref names can be controlled by an attacker, so these values are substituted into the script before bash parses it. Use the existing $GITHUB_REF_NAME, $GITHUB_REF and $GITHUB_BASE_REF env vars instead.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, PYTHON_VERSION comes from inputs.python-version and is expanded without quotes in a case statement: `case $PYTHON_VERSION in`. It should be `case "$PYTHON_VERSION" in`.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes `echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"`. These values come from workflow-controlled sources: CU_VERSION, ARCH and PYTHON_VERSION come from inputs, and REPOSITORY and REF are inherited process env vars. They are written without the `printf '%s' ... | tr -d '\n\r'` sanitization step, so a value containing a newline could inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). Moved github.ref_name/event.ref/ref/base_ref expressions into step env vars in the 'Log Available Webhook Fields' step. Quoted $PYTHON_VERSION in the case statement. ARTIFACT_NAME is now built into a variable and stripped of newlines with printf|tr before being written to GITHUB_ENV.

