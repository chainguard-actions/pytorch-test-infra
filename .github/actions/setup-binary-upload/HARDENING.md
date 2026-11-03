<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

In the composite step 'Set the artifact name', values from inputs.repository, inputs.ref, inputs.python-version, inputs.cuda-version and inputs.arch are passed in through env vars (REPOSITORY, REF, PYTHON_VERSION, CU_VERSION, ARCH). They are then written to $GITHUB_ENV without the printf '%s' ... | tr -d '\n\r' cleanup: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". If a value contains a newline, the caller can add any environment variable they want.

Locations:

- `action.yml:58`

### unpinned-uses (severity: high)

Two composite steps reference actions by mutable tag instead of a full 40-character commit SHA: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:36`
- `action.yml:61`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses

**Notes:**

The 'Set the artifact name' step now builds ARTIFACT_NAME first, removes newlines and carriage returns with printf '%s' | tr -d '\n\r', and only then writes it to $GITHUB_ENV. actions/setup-python is pinned to a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). Both SHAs came from lookup_action_sha. No other lines changed. Nothing was run or tested, and no re-analysis was done after the edits.

### Iteration 2

**Fixes applied:** unpinned-uses, github-env-injection, script-injection

**Notes:**

Pinned actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). Put double quotes around the pip install path. BUILD_ENV_FILE now goes through printf | tr -d '\n\r' before it is written to GITHUB_ENV. Also repaired the ARTIFACT_NAME echo line, which an earlier pass had mangled into 'ARTIFACT_NAactions/checkout@... # v4NAME}'. It is now echo "ARTIFACT_NAME=${SAFE_ARTIFACT_NAME}" >> "${GITHUB_ENV}".

