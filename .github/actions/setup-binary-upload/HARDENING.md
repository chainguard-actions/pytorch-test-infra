<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20260922-155642** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by mutable tag instead of a full 40-character commit SHA: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

The step 'Set the artifact name' writes values from inputs to $GITHUB_ENV without sanitizing them first. The values are inputs.repository, inputs.ref, inputs.python-version, inputs.cuda-version and inputs.arch, passed in as the REPOSITORY, REF, PYTHON_VERSION, CU_VERSION and ARCH env vars. The offending line is: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". Replacing '/' does not remove newlines or carriage returns. A value containing a newline could therefore add arbitrary environment variables. The fix is to build the value and run it through printf '%s' ... | tr -d '\n\r' right before the write.

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). In the 'Set the artifact name' step, ARTIFACT_NAME is now built into a variable and passed through printf '%s' | tr -d '\n\r' before it is written to GITHUB_ENV. The step already runs under bash with pipefail, so a failure is still reported. I haven't run the action after these changes.

