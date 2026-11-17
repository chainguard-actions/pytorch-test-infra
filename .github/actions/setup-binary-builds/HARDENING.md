<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has `uses:` references pinned to tags, not full commit SHAs: `uses: actions/checkout@v4` and `uses: conda-incubator/setup-miniconda@v3.1.1`. Pin each one to a 40-character commit SHA.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run script: `echo "${{ github.ref_name }}"`, `echo "${{ github.event.ref }}"`, `echo "${{ github.ref }}"`, `echo "${{ github.base_ref }}"`. Values like branch names can be attacker-controlled. Use the env vars instead ($GITHUB_REF_NAME, $GITHUB_REF, $GITHUB_BASE_REF), which the same step already prints.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, the env var PYTHON_VERSION, which comes from inputs.python-version, is expanded without quotes in `case $PYTHON_VERSION in`. It must be double-quoted: `case "$PYTHON_VERSION" in`.

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes untrusted values to $GITHUB_ENV without the `printf '%s' ... | tr -d '\n\r'` sanitization step: `echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"`. CU_VERSION and ARCH come from inputs, SHORT_PYTHON_VERSION is derived from inputs.python-version, and REPOSITORY and REF are inherited from the calling workflow's env. A newline in any of them lets an attacker inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

All four findings are fixed in action.yml. I haven't run the action to test the changes.

- **unpinned-uses:** actions/checkout is now pinned to commit 11d5960a326750d5838078e36cf38b85af677262 (tag v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (tag v3.1.1). The tag is kept as a trailing comment on each line.
- **script-injection, 'Log Available Webhook Fields' step:** the four github.* expressions (ref_name, event.ref, ref, base_ref) now go through the step's env: block and are echoed as plain variables. The finding suggested reusing the runner's own GITHUB_REF_NAME, GITHUB_REF and GITHUB_BASE_REF instead; I didn't, so the 'GITHUB PROVIDED' lines still print what upstream printed, including github.event.ref, which has no runner variable.
- **script-injection, 'Setup conda environment for build' step:** the case statement now quotes the variable: `case "$PYTHON_VERSION" in`.
- **github-env-injection, 'Set artifact name' step:** the artifact name is now built into a variable first, newlines are stripped with `printf '%s' | tr -d '\n\r'`, and only then is it written to GITHUB_ENV. This doesn't hide a failure: building the name runs no command, and the step already uses pipefail.

