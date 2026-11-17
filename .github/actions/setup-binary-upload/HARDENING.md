<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261109-232755** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps use mutable tag refs instead of full 40-character commit SHAs: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:36`
- `action.yml:63`

### github-env-injection (severity: high)

Step 'Set the artifact name' writes values taken from inputs (REPOSITORY, REF, CU_VERSION, ARCH from inputs.*, plus SHORT_PYTHON_VERSION built from inputs.python-version) to $GITHUB_ENV without first running them through printf '%s' ... | tr -d '\n\r'. Offending line: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A newline in any of these inputs could add arbitrary environment variables for later steps.

Locations:

- `action.yml:60`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). ARTIFACT_NAME is now built into a variable first, run through printf '%s' | tr -d '\n\r', and only then written to $GITHUB_ENV.

