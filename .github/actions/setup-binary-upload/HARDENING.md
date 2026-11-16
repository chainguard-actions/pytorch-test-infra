<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261109-192709** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Set the artifact name' writes a value built from untrusted inputs (inputs.repository, inputs.ref, inputs.python-version, inputs.cuda-version, inputs.arch, passed in through env vars REPOSITORY/REF/PYTHON_VERSION/CU_VERSION/ARCH) to $GITHUB_ENV. Nothing strips newlines first (no printf '%s' ... | tr -d '\n\r'): echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". An input that contains a newline can inject extra environment variables into later steps.

Locations:

- `action.yml:58`

### unpinned-uses (severity: high)

Composite action steps use tag refs instead of full 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses

**Notes:**

Strips CR/LF from ARTIFACT_NAME (printf '%s' | tr -d '\n\r') before writing it to GITHUB_ENV. Pinned actions/setup-python@v5 -> a26af69be951a213d495a4c3e4e4022e16d87065 and actions/checkout@v4 -> 11d5960a326750d5838078e36cf38b85af677262, keeping the tag as a comment.

