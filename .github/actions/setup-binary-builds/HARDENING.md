<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261021-234439** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}" and echo "${{ github.base_ref }}". Branch and tag names can be chosen by an attacker, so these values can inject shell commands.

Locations:

- `action.yml:72`

### script-injection (severity: high)

Rule (b): the 'Setup conda environment for build' step expands the input-derived env var without quotes: `case $PYTHON_VERSION in`. The '# shellcheck disable=SC2153' comment above it does not make this an exempt array assignment. It should be `case "$PYTHON_VERSION" in`.

Locations:

- `action.yml:162`

### github-env-injection (severity: high)

The 'Set artifact name' step writes `echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"` without sanitizing it first. CU_VERSION and ARCH come from inputs.*. SHORT_PYTHON_VERSION is derived from inputs.python-version. REPOSITORY and REF are inherited process env vars that this step does not set. None of these go through printf '%s' ... | tr -d '\n\r' before the write, so a newline in any of them can inject extra environment variables.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

Two composite steps reference actions by tag instead of a full commit SHA: `uses: actions/checkout@v4` (line 56) and `uses: conda-incubator/setup-miniconda@v3.1.1` (line 93).

Locations:

- `action.yml:56`
- `action.yml:93`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection, unpinned-uses

**Notes:**

I fixed all four findings in hardened/action/action.yml.

1. Log Available Webhook Fields step: the four values (github.ref_name, github.event.ref, github.ref, github.base_ref) are now set in the step's env: block. The script reads them as quoted shell variables instead of having them pasted into it.
2. Setup conda environment for build step: `case $PYTHON_VERSION` is now quoted as `case "$PYTHON_VERSION"`.
3. Set artifact name step: the ARTIFACT_NAME value is now built first, then newlines are stripped with printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV. REPOSITORY and REF still come from the caller's environment, as they did upstream.
4. Pinned actions/checkout v4 to 11d5960a326750d5838078e36cf38b85af677262 and conda-incubator/setup-miniconda v3.1.1 to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830. Both SHAs came from lookup_action_sha, and each line keeps the tag as a comment.

Nothing has been run to test these changes.

