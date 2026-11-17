<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that reference actions by mutable tag instead of a full 40-character commit SHA: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

Step 'Set the artifact name' writes a value built from inputs.repository, inputs.ref, inputs.python-version, inputs.cuda-version and inputs.arch (passed in through the env vars REPOSITORY, REF, PYTHON_VERSION, CU_VERSION, ARCH) to $GITHUB_ENV without sanitising it first: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". The '/' replacement does not remove newlines, so an input containing a newline can add arbitrary environment variables. Fix: clean the value with printf '%s' ... | tr -d '\n\r' before writing it.

Locations:

- `action.yml:58`

### github-env-injection (severity: high)

Step 'Generate env variables from pytorch_pkg_helpers' writes BUILD_ENV_FILE to $GITHUB_ENV without sanitising it first: echo "BUILD_ENV_FILE=${BUILD_ENV_FILE}" >> "${GITHUB_ENV}". BUILD_ENV_FILE is built from RUNNER_TEMP, a process env var the composite action inherits and does not set in this script, so the check counts it as workflow-controlled. Fix: run it through printf '%s' "$BUILD_ENV_FILE" | tr -d '\n\r' before the write.

Locations:

- `action.yml:85`

### script-injection (severity: high)

Rule (b): an env var expansion is not quoted in the composite step 'Generate env variables from pytorch_pkg_helpers': 'python -m pip install ${GITHUB_WORKSPACE}/test-infra/tools/pkg-helpers'. Quote it as "${GITHUB_WORKSPACE}/test-infra/tools/pkg-helpers".

Locations:

- `action.yml:79`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection, script-injection

**Notes:**

Pinned actions/setup-python@v5 to a26af69be951a213d495a4c3e4e4022e16d87065 and actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262, keeping the tag in a comment after each SHA. Before ARTIFACT_NAME and BUILD_ENV_FILE are written to $GITHUB_ENV, each value now goes through printf '%s' | tr -d '\n\r' to remove newlines. Both values are built from plain variables, not command output, so the sanitising can't hide a failed command. Quoted the ${GITHUB_WORKSPACE} path in the pip install command. I haven't run the action to test these changes.

