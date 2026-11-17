<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261109-192709** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that point to version tags instead of full 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

The 'Set the artifact name' step builds ARTIFACT_NAME from inputs.repository, inputs.ref, inputs.cuda-version and inputs.arch. These reach the step through env vars REPOSITORY, REF, CU_VERSION and ARCH. It writes the result to $GITHUB_ENV without running printf '%s' ... | tr -d '\n\r' first: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A newline in any of these inputs would let a caller add arbitrary environment variables.

Locations:

- `action.yml:58`

### script-injection (severity: high)

Rule (b): in the 'Generate env variables from pytorch_pkg_helpers' step, an inherited env var is expanded without quotes: 'python -m pip install ${GITHUB_WORKSPACE}/test-infra/tools/pkg-helpers'. Env vars in composite run blocks must be treated as untrusted, so this expansion should be double-quoted.

Locations:

- `action.yml:79`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection, script-injection

**Notes:**

I fixed all three findings in action.yml. The changes have not been run or tested.
- unpinned-uses: actions/setup-python is now pinned to a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). Both SHAs came from lookup_action_sha.
- github-env-injection: the 'Set the artifact name' step builds the artifact name into a variable first, strips newlines and carriage returns from it with printf '%s' | tr -d '\n\r', and only then writes ARTIFACT_NAME to GITHUB_ENV. The name is otherwise built the same way as before.
- script-injection: the path ${GITHUB_WORKSPACE}/test-infra/tools/pkg-helpers in the pip install command is now in double quotes.

