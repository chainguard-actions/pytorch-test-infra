<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to mutable tags instead of full commit SHAs: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". The values are substituted before the shell parses the script, so a crafted ref or branch name can inject commands. Fix: pass them through env vars or use the GITHUB_REF_NAME, GITHUB_REF and GITHUB_BASE_REF env vars, double-quoted.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): the 'Setup conda environment for build' step expands PYTHON_VERSION without quotes in 'case $PYTHON_VERSION in'. PYTHON_VERSION comes from inputs.python-version. It should be quoted as case "$PYTHON_VERSION" in.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes workflow-controlled values to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". CU_VERSION and ARCH come from inputs. SHORT_PYTHON_VERSION comes from inputs.python-version. REPOSITORY and REF are inherited from the calling workflow's environment because this step doesn't set them. A value containing a newline can inject arbitrary environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

I pinned actions/checkout to the full commit SHA for v4 and conda-incubator/setup-miniconda to the SHA for v3.1.1, keeping the tag names as comments. In the 'Log Available Webhook Fields' step, the four github.* expressions are now passed in through env vars and echoed double-quoted. I changed 'case $PYTHON_VERSION' to 'case "$PYTHON_VERSION"'. The ARTIFACT_NAME value is now built first and has newlines and carriage returns stripped (printf '%s' | tr -d '\n\r') before it is written to GITHUB_ENV. All changes are in action.yml; I did not run the action to test them.

