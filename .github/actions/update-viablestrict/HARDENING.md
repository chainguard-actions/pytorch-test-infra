<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261109-192709** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that use mutable tags instead of full commit SHAs: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): step 'Get latest viable commit' puts an expression straight into the run script: '--required-checks "${{ inputs.requires }}"'. A crafted 'requires' input can break out of the quotes and run commands. Rule (b): the same step also expands workflow-influenced data without quotes, in 'python ${TEST_INFRA_PATH}/tools/...' and 'echo $output'. The fix is to pass inputs.requires through an env var and double-quote every expansion.

Locations:

- `action.yml:94`
- `action.yml:93`
- `action.yml:98`

### script-injection (severity: high)

Rule (b): step 'Push SHA to viable/strict branch' expands push_result without quotes in 'echo $push_result'. push_result is git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values.

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

Step 'Get latest viable commit' writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output comes from a script run with the untrusted inputs.requires value, and it is not sanitized first with printf '%s' ... | tr -d '\n\r'.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

Step 'Push SHA to viable/strict branch' writes push_result to $GITHUB_OUTPUT with a heredoc ('echo push_result<<EOF; echo $push_result; echo EOF'). push_result is git output built from the workflow-controlled STABLE_BRANCH input and the LATEST_VIABLE_SHA step output, and it is not sanitized first with printf '%s' ... | tr -d '\n\r'.

Locations:

- `action.yml:117`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python and actions/checkout to full commit SHAs. Moved inputs.requires into env (REQUIRES) and quoted the script path and echo expansions. latest_viable_sha is now sanitized with tr -d '\n\r' before it is written to GITHUB_OUTPUT. push_result now uses a random delimiter from /dev/urandom in place of the fixed EOF. Its value is collapsed onto one line, as upstream's unquoted echo did, so the output keeps the same format.

