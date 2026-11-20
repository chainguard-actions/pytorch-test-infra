<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261119-192116** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to mutable tags instead of 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

The 'Set the artifact name' step builds ARTIFACT_NAME from values taken from inputs.* (REPOSITORY, REF, CU_VERSION, ARCH, and SHORT_PYTHON_VERSION, which comes from PYTHON_VERSION) and writes it to $GITHUB_ENV. Nothing runs printf '%s' ... | tr -d '\n\r' on the value first: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". An input containing a newline could add arbitrary environment variables. The sed call on PYTHON_VERSION works line by line, so it does not reliably strip newlines either.

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in hardened/action/action.yml. Nothing was run to test the changes.

- **unpinned-uses:** `actions/setup-python` is now pinned to commit a26af69be951a213d495a4c3e4e4022e16d87065 (# v5), and `actions/checkout` to 11d5960a326750d5838078e36cf38b85af677262 (# v4). Both SHAs came from lookup_action_sha.
- **github-env-injection:** the 'Set the artifact name' step now builds the full ARTIFACT_NAME value first. It then removes newline and carriage-return characters with `printf '%s' ... | tr -d '\n\r'` before writing to $GITHUB_ENV. This covers every input that goes into the name, including the python-version value after sed has processed it.

All other steps are unchanged.

