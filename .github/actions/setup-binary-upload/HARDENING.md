<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261021-234439** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses actions by tag, not by a full commit SHA: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

The 'Set the artifact name' step writes values built from inputs to $GITHUB_ENV without the sanitization step (printf '%s' ... | tr -d '\n\r'). The values are REPOSITORY, REF, CU_VERSION, ARCH and PYTHON_VERSION (through SHORT_PYTHON_VERSION), all routed through env. Offending line: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A newline in any of these inputs could inject extra environment variables, such as LD_PRELOAD or PATH, into later steps.

Locations:

- `action.yml:58`

### script-injection (severity: high)

Rule (b): an env var is expanded without quotes in the 'Generate env variables from pytorch_pkg_helpers' step. Offending line: python -m pip install ${GITHUB_WORKSPACE}/test-infra/tools/pkg-helpers. The fix is to quote it: "${GITHUB_WORKSPACE}/test-infra/tools/pkg-helpers".

Locations:

- `action.yml:79`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection, script-injection

**Notes:**

All three findings are fixed in action.yml. Nothing was run to test the changes.

- **unpinned-uses:** `actions/setup-python` is now pinned to commit a26af69be951a213d495a4c3e4e4022e16d87065 and `actions/checkout` to 11d5960a326750d5838078e36cf38b85af677262. Both SHAs came from looking up the current `v5` and `v4` tags, and the tag names are kept as trailing comments.
- **github-env-injection:** the 'Set the artifact name' step now builds `ARTIFACT_NAME` in a local variable first. It strips newlines and carriage returns with `printf '%s' ... | tr -d '\n\r'` before writing the line to `$GITHUB_ENV`.
- **script-injection:** `${GITHUB_WORKSPACE}/test-infra/tools/pkg-helpers` is now double-quoted in the `pip install` command.

