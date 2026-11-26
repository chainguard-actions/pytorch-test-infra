<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261125-223308** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses actions by mutable tags rather than full 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

Step 'Set the artifact name' writes a value built from untrusted inputs (REPOSITORY, REF, PYTHON_VERSION, CU_VERSION, ARCH, all taken from inputs.* through env:) to $GITHUB_ENV with no newline sanitization: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A value containing a newline can inject extra environment variables. Before the write, pass the value through printf '%s' ... | tr -d '\n\r'.

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). In the 'Set the artifact name' step, the artifact name is now built in a variable first. Newlines and carriage returns are stripped with printf | tr -d '\n\r', and only then is it written to GITHUB_ENV. The value written for normal inputs is unchanged.

