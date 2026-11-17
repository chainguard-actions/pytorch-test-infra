<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

These action references in action.yml use a mutable tag instead of a full 40-character commit SHA: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions directly into the run: script. The lines are: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}" and echo "${{ github.base_ref }}". Branch and ref names can be controlled by an attacker. Because the template is filled in before the shell runs, these values can inject commands. Pass them through env: variables and quote them in the script.

Locations:

- `action.yml:71`
- `action.yml:72`
- `action.yml:73`
- `action.yml:74`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, the env var PYTHON_VERSION (from inputs.python-version) is expanded unquoted: 'case $PYTHON_VERSION in'. The shellcheck SC2153 directive above it does not qualify for an exemption. Change it to 'case "$PYTHON_VERSION" in'.

Locations:

- `action.yml:152`

### github-env-injection (severity: high)

The 'Set artifact name' step writes workflow-controlled values to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' sanitization step. The line is: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". CU_VERSION and ARCH come from inputs.*, and SHORT_PYTHON_VERSION comes from inputs.python-version. REPOSITORY and REF are inherited process env vars that this step does not set. A newline in any of these values lets an attacker add extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

Pinned actions/checkout to 11d5960a… (v4) and conda-incubator/setup-miniconda to 505e6394… (v3.1.1). In 'Log Available Webhook Fields', the github.ref_name/event.ref/ref/base_ref expressions now come in through env vars and are quoted in the script. Quoted $PYTHON_VERSION in the case statement. ARTIFACT_NAME now has \n and \r stripped with printf | tr before it is written to GITHUB_ENV.

