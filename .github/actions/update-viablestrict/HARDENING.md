<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261109-192709** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite steps reference actions by mutable tag rather than full commit SHA: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Step 'Get latest viable commit': (a) expression interpolated directly into run script: '--required-checks "${{ inputs.requires }}"'. The input should be passed through an env: variable and referenced as "$REQUIRES". (b) 'echo $output' expands the script output unquoted. That output comes from the requires input and ClickHouse data.

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Step 'Push SHA to viable/strict branch': (b) unquoted expansion 'echo $push_result'. push_result holds git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. It should be quoted as "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

Step 'Get latest viable commit' writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output comes from a script run with untrusted input (inputs.requires) and remote data, and it is written without the printf '%s' ... | tr -d '\n\r' sanitization step.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

Step 'Push SHA to viable/strict branch' writes push_result to $GITHUB_OUTPUT using a fixed 'EOF' heredoc delimiter, with no sanitization. push_result contains git output built from inputs.stable-branch and the steps output LATEST_VIABLE_SHA. A crafted value with newlines or 'EOF' could inject extra outputs.

Locations:

- `action.yml:118`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python and actions/checkout to full commit SHAs. Moved inputs.requires into the REQUIRES env var and quoted it where it is used. Quoted the script path and the echoes of $output and $push_result. Newlines are now stripped from latest_viable_sha before it is written to GITHUB_OUTPUT. The fixed EOF delimiter for push_result is replaced with a random one drawn from /dev/urandom, and the multi-line value is written as is. One visible change: push_result used to be flattened onto one line by the unquoted echo, and it now keeps git's original line breaks.

