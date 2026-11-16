<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

These uses: refs in action.yml point to a mutable tag instead of a full 40-character commit SHA: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92). Pin each one to its commit SHA.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run: script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". Branch and ref names can contain shell metacharacters, so an attacker could run commands. Pass these values through env: variables, or use the GITHUB_REF_NAME, GITHUB_REF and GITHUB_BASE_REF env vars the runner already sets.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, PYTHON_VERSION comes from inputs.python-version but is expanded without quotes as a case subject: 'case $PYTHON_VERSION in'. The shellcheck directive above it disables SC2153, not SC2086/SC2206, and this is not an array assignment, so the exemption does not apply. Change it to 'case "$PYTHON_VERSION" in'.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"' with no printf '%s' ... | tr -d '\n\r' step first. CU_VERSION and ARCH come from inputs. SHORT_PYTHON_VERSION comes from inputs.python-version through a sed that does not strip newlines. REPOSITORY and REF are not set in this step, so they are inherited from the calling workflow's env. A newline in any of them could inject extra environment variables. Strip newlines before the write.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). Moved github.ref_name, github.event.ref, github.ref and github.base_ref out of the 'Log Available Webhook Fields' script and into env: variables. Quoted the case subject ("$PYTHON_VERSION"). The ARTIFACT_NAME value now goes through printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV. As in upstream, REPOSITORY and REF still come from the calling workflow's environment. Nothing was run to test these changes.

