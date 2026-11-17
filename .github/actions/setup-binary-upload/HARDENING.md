<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261112-155209** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by mutable tag, not by a full commit SHA: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

The 'Set the artifact name' step builds ARTIFACT_NAME from env vars that come from inputs (REPOSITORY, REF, CU_VERSION, ARCH, and SHORT_PYTHON_VERSION derived from inputs.python-version). It writes the value to $GITHUB_ENV with no sanitization: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". Nothing like printf '%s' ... | tr -d '\n\r' is applied first, so a value containing a newline can inject extra environment variables.

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). ARTIFACT_NAME is now built in a variable and passed through printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV. Nothing was run to test these changes.

