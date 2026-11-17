<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has `uses:` references pinned to tags, not full commit SHAs: `uses: actions/checkout@v4` (line 55) and `uses: conda-incubator/setup-miniconda@v3.1.1` (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run script: `echo "${{ github.ref_name }}"`, `echo "${{ github.event.ref }}"`, `echo "${{ github.ref }}"`, `echo "${{ github.base_ref }}"`. Branch and ref names can be controlled by an attacker, and the values are substituted before the shell parses the script.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, `case $PYTHON_VERSION in` expands the env var PYTHON_VERSION without quotes. Its value comes from inputs.python-version. It should be written as `case "$PYTHON_VERSION" in`. The `# shellcheck disable=SC2153` directive above it does not trigger the array-assignment exemption.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes `echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"`. CU_VERSION and ARCH come from inputs.cuda-version and inputs.arch. REPOSITORY and REF are process env vars inherited from the calling workflow. SHORT_PYTHON_VERSION comes from inputs.python-version. None of these values go through `printf '%s' ... | tr -d '\n\r'` before the write, so a newline in any of them could inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Fixed every finding in action.yml. Nothing was run or tested after the edits.

- unpinned-uses: pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). Both SHAs came from lookups, and the tag is kept in a trailing comment.
- script-injection: the four github.* ref expressions in the 'Log Available Webhook Fields' step now go through env vars (GH_REF_NAME, GH_EVENT_REF, GH_REF, GH_BASE_REF) and are echoed in double quotes. In the conda setup step, `case $PYTHON_VERSION in` is now `case "$PYTHON_VERSION" in`.
- github-env-injection: ARTIFACT_NAME is now assembled into a variable and passed through `printf '%s' ... | tr -d '\n\r'` before it is written to GITHUB_ENV, so a newline in any input can't add extra environment variables. The step runs with `set -euxo pipefail`, so a failure inside the pipeline still stops it.

