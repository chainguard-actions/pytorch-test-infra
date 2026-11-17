<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Set the artifact name' writes a value built from untrusted inputs (inputs.repository, inputs.ref, inputs.cuda-version, inputs.arch, and inputs.python-version via SHORT_PYTHON_VERSION) to $GITHUB_ENV. They pass through env vars but are never sanitized with printf '%s' ... | tr -d '\n\r' before the write: `echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"`. A newline in any of these values lets a caller inject extra environment variables.

Locations:

- `action.yml:58`

### unpinned-uses (severity: high)

Two composite steps reference actions by a mutable tag instead of a full 40-character commit SHA: `uses: actions/setup-python@v5` and `uses: actions/checkout@v4`.

Locations:

- `action.yml:36`
- `action.yml:61`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses

**Notes:**

I fixed both findings in action.yml.

- github-env-injection: the 'Set the artifact name' step now builds the artifact name in a variable, removes newline and carriage-return characters with printf '%s' | tr -d '\n\r', and only then writes ARTIFACT_NAME to $GITHUB_ENV. Any newline in the repository, ref, Python version, CUDA version or arch inputs is now removed before the write, so a caller can't add extra environment variables. Normal values come out the same as before.
- unpinned-uses: I looked up the full commit SHAs and pinned both actions, keeping the tag as a comment: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5 and actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.

Nothing was run or tested after the edits.

### Iteration 2

**Fixes applied:** script-injection, github-env-injection

**Notes:**

I fixed both findings in action.yml, in the 'Generate env variables from pytorch_pkg_helpers' step. Nothing was run to test the changes.

1. script-injection: the pip install path is now in double quotes ("${GITHUB_WORKSPACE}/test-infra/tools/pkg-helpers"), so the shell can't split it on spaces or expand it as a pattern.

2. github-env-injection: BUILD_ENV_FILE now has newline and carriage-return characters stripped (printf '%s' ... | tr -d '\n\r') into SAFE_BUILD_ENV_FILE, and that cleaned value is what gets written to $GITHUB_ENV. The variable still points to the same file, and the step's other commands still use the original BUILD_ENV_FILE.

