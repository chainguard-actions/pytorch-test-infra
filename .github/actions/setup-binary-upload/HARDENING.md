<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261118-220128** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite steps reference actions by mutable tag instead of a full 40-char commit SHA: line 36 'uses: actions/setup-python@v5' and line 61 'uses: actions/checkout@v4'.

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

Step 'Set the artifact name' writes values built from inputs (REPOSITORY, REF, PYTHON_VERSION via SHORT_PYTHON_VERSION, CU_VERSION, ARCH, all from inputs.*) to $GITHUB_ENV without the required sanitization (printf '%s' ... | tr -d '\n\r'): 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"'. A newline in any of these inputs could inject arbitrary environment variables (e.g. LD_PRELOAD, BASH_ENV) into later steps.

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/setup-python@v5 to a26af69be951a213d495a4c3e4e4022e16d87065 and actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262, each with a comment naming the original tag. The ARTIFACT_NAME value is now built in a variable first, then has CR and LF stripped with printf '%s' | tr -d '\n\r' before it is written to $GITHUB_ENV. Inputs were already passed in through env:, so no shell rewrite was needed.

