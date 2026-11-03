<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261027-001733** was hardened automatically. 6 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action references actions by mutable tag instead of a 40-character commit SHA: 'uses: actions/setup-python@v5' (line 63) and 'uses: actions/checkout@v4' (line 67).

Locations:

- `action.yml:63`
- `action.yml:67`

### script-injection (severity: high)

Step 'Get latest viable commit' breaks rule (a): an expression is placed straight into the run script: '--required-checks "${{ inputs.requires }}"' (line 95). The inputs.requires value is pasted into the shell script before bash runs it, so it can inject commands. Move it into an env: variable and expand it as "$REQUIRES". The same step also breaks rule (b): 'python ${TEST_INFRA_PATH}/tools/...' (line 94) and 'echo $output' (line 99) expand variables without double quotes.

Locations:

- `action.yml:95`
- `action.yml:99`

### script-injection (severity: high)

Step 'Push SHA to viable/strict branch' breaks rule (b): 'echo $push_result' (line 120) expands a variable without double quotes. push_result holds git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values, so the shell can word-split and glob-expand it. Quote it as "$push_result".

Locations:

- `action.yml:120`

### github-env-injection (severity: high)

Step 'Get latest viable commit' writes '$output' to GITHUB_OUTPUT with 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' (line 98) without sanitizing it first. The value is the output of a script driven by inputs.requires and the checked-out repository. The printf '%s' ... | tr -d '\n\r' step is missing, so a value containing newlines could inject extra outputs.

Locations:

- `action.yml:98`

### github-env-injection (severity: high)

Step 'Push SHA to viable/strict branch' writes push_result to GITHUB_OUTPUT with a fixed 'EOF' heredoc delimiter (lines 118-122) without sanitizing it. push_result is git output that includes the input-controlled STABLE_BRANCH and the upstream step output LATEST_VIABLE_SHA. With no printf '%s' ... | tr -d '\n\r' step and a predictable delimiter, a crafted value could close the heredoc early and inject extra outputs.

Locations:

- `action.yml:117`
- `action.yml:122`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (# v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (# v4). Moved inputs.requires into env REQUIRES and the script now uses "$REQUIRES". Put double quotes around the script path and around the echo of $output. latest_viable_sha now has newlines removed (printf | tr -d) before it is written to GITHUB_OUTPUT; the command is still captured on its own, so a failure still stops the step. push_result now uses a random delimiter read from /dev/urandom, and its value is written quoted. Newlines in it become spaces, which keeps upstream's single-line output (the old unquoted echo also flattened it to one line).

### Iteration 2

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In 'Push SHA to viable/strict branch', the fixed 'EOF' heredoc delimiter is replaced with a random one from /dev/urandom, and push_result is written double-quoted via printf '%s\n' instead of the unquoted 'echo $push_result'. This keeps the value's lines intact (the multi-line heredoc form) while preventing delimiter breakout, word-splitting, and glob expansion.

