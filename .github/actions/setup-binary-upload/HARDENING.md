<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261125-022556** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Set the artifact name' writes values taken from inputs (inputs.repository, inputs.ref, inputs.cuda-version, inputs.arch, and inputs.python-version through SHORT_PYTHON_VERSION) to $GITHUB_ENV without first passing them through printf '%s' ... | tr -d '\n\r'. The line is: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A newline in any of these inputs lets the caller inject extra environment variables (for example LD_PRELOAD or PATH) into every later step.

Locations:

- `action.yml:58`

### unpinned-uses (severity: high)

The composite steps reference actions by mutable tags instead of full 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses

**Notes:**

I fixed both findings in action.yml.

1. github-env-injection: the 'Set the artifact name' step now builds ARTIFACT_NAME into a local variable first, strips newlines and carriage returns with printf '%s' | tr -d '\n\r', and only then writes it to $GITHUB_ENV. The name is built exactly as before.
2. unpinned-uses: actions/setup-python@v5 is now pinned to a26af69be951a213d495a4c3e4e4022e16d87065 # v5, and actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262 # v4. Both SHAs came from lookup_action_sha.

I haven't run the action after these changes.

