<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261123-205410** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by tag, not by a full 40-character commit SHA: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". Ref names can be controlled by an attacker, and these values are inserted into the script before the shell parses it.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): the 'Setup conda environment for build' step expands the input-derived env var PYTHON_VERSION (from inputs.python-version) without quotes: 'case $PYTHON_VERSION in'. It should be 'case "$PYTHON_VERSION" in'.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes input-derived values (CU_VERSION from inputs.cuda-version, ARCH from inputs.arch, SHORT_PYTHON_VERSION from inputs.python-version) and env vars inherited from the calling workflow (REPOSITORY, REF) to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' cleanup step: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A newline in any of these values could inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a… (v4) and conda-incubator/setup-miniconda to 505e6394… (v3.1.1). Moved the github.ref_name, event.ref, ref and base_ref expressions into env vars in the logging step. Quoted $PYTHON_VERSION in the case statement. ARTIFACT_NAME is now built in a variable and stripped of CR/LF with printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV.

