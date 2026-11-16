<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261029-163400** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by mutable tag instead of a full 40-character commit SHA: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

The 'Set the artifact name' step writes values built from inputs.repository, inputs.ref, inputs.python-version, inputs.cuda-version and inputs.arch to $GITHUB_ENV. These arrive through the env vars REPOSITORY, REF, PYTHON_VERSION, CU_VERSION and ARCH, and nothing strips newlines first: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A newline in any of these values can inject extra environment variables. Clean the composed value with printf '%s' ... | tr -d '\n\r' before writing it.

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/setup-python@v5 to a26af69be951a213d495a4c3e4e4022e16d87065 and actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262, each with its tag kept in a trailing comment. In the 'Set the artifact name' step, the ARTIFACT_NAME value is now built first, then cleaned with printf '%s' | tr -d '\n\r' before it's written to GITHUB_ENV. Not tested. Not touched: BUILD_ENV_FILE in the last step is also written to GITHUB_ENV, but it's built only from runner variables, not inputs, so it wasn't flagged.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

Sanitized BUILD_ENV_FILE with printf '%s' | tr -d '\n\r' before writing to $GITHUB_ENV in the 'Generate env variables from pytorch_pkg_helpers' step.

