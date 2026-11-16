<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261021-234439** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references actions by mutable tags instead of full commit SHAs: 'uses: actions/setup-python@v5' (line 36) and 'uses: actions/checkout@v4' (line 61).

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

Step 'Set the artifact name' builds ARTIFACT_NAME from the env vars REPOSITORY, REF, PYTHON_VERSION, CU_VERSION and ARCH, all set from inputs.*, and writes it to $GITHUB_ENV with no newline sanitization first: echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". If an input contains a newline, the caller can inject any environment variable. The sed call does not strip newlines from SHORT_PYTHON_VERSION, and the other values are not filtered at all. Run each value through printf '%s' ... | tr -d '\n\r' before the write.

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I pinned actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). Both commit SHAs were looked up with lookup_action_sha. In the 'Set the artifact name' step, ARTIFACT_NAME is now built first, and newlines and carriage returns are stripped from it with printf '%s' | tr -d '\n\r'. Only then is it written to $GITHUB_ENV. The last step's BUILD_ENV_FILE write was left alone: its value comes from runner variables, not from inputs. Nothing was run or tested.

