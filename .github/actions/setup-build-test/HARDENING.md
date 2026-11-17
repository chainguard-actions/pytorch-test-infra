<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-build-test/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-build-test/v20261021-234439** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step pins its action to a tag, not a full 40-character commit SHA: `uses: actions/checkout@v4`. Pin it to a commit SHA.

Locations:

- `action.yml:36`

### github-env-injection (severity: high)

The step 'Setup useful environment variables' writes an inherited process env var to $GITHUB_ENV without the sanitization step: `echo "RUNNER_ARTIFACT_DIR=${RUNNER_TEMP}/artifacts" >> "${GITHUB_ENV}"`. RUNNER_TEMP is set outside this run: script, and composite actions inherit env from the calling workflow. Under the check's rule it counts as untrusted, so strip newlines first: safe=$(printf '%s' "${RUNNER_TEMP}/artifacts" | tr -d '\n\r').

Locations:

- `action.yml:45`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Pinned actions/checkout@v4 to 11d5960a326750d5838078e36cf38b85af677262. Sanitized RUNNER_TEMP-derived value with tr -d '\n\r' before writing RUNNER_ARTIFACT_DIR to GITHUB_ENV.

