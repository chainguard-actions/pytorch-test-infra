<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261118-220128** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has 2 actions referenced by a version tag instead of a full 40-character commit SHA: line 55 `uses: actions/checkout@v4` and line 92 `uses: conda-incubator/setup-miniconda@v3.1.1`. A tag can be moved to point at different code, so these should be pinned to commit SHAs.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run script, e.g. `echo "${{ github.ref_name }}"`, `echo "${{ github.event.ref }}"`, `echo "${{ github.ref }}"` and `echo "${{ github.base_ref }}"`. A branch or tag name is controlled by whoever creates it, and the shell runs whatever ends up in the script. Pass these through env variables, or use the GITHUB_REF_NAME, GITHUB_REF and GITHUB_BASE_REF variables the runner already sets.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, `case $PYTHON_VERSION in` expands PYTHON_VERSION (set from inputs.python-version) without double quotes. It should be `case "$PYTHON_VERSION" in`. The `# shellcheck disable=SC2153` comment above it does not cover this: the array-assignment exception only applies to SC2086/SC2206 on NAME=($VAR) lines.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes `echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"`. Some of these values come from inputs (python-version, cuda-version, arch). REPOSITORY and REF are not set anywhere in this step, so they come from the calling workflow's environment. None of them have newlines stripped before the write, so a value containing a newline can add extra variables to GITHUB_ENV. Run `printf '%s' ... | tr -d '\n\r'` on the value before writing it.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout (v4) and conda-incubator/setup-miniconda (v3.1.1) to full commit SHAs. In the 'Log Available Webhook Fields' step, the github.* expressions now pass through env vars. In the conda setup step, PYTHON_VERSION is now quoted in the case statement. In 'Set artifact name', the ARTIFACT_NAME value has CR/LF stripped with printf | tr before it is written to GITHUB_ENV. REPOSITORY and REF still come from the calling workflow's environment, the same as upstream.

