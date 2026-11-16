<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20260922-155642** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps whose uses: refs are tags, not full commit SHAs: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66). Pin each one to a 40-character commit SHA.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression straight into the run script: '--required-checks "${{ inputs.requires }}" \'. The caller controls inputs.requires, and the value is pasted into the bash script before the shell runs it, so it can inject commands. Move it into an env: variable (e.g. REQUIRES) and use "$REQUIRES". Rule (b): the same step also expands workflow-derived data unquoted: 'echo $output' (line 98) and the unquoted ${TEST_INFRA_PATH} on line 93.

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Rule (b): the 'Push SHA to viable/strict branch' step expands push_result unquoted: 'echo $push_result'. push_result holds git output that includes the caller-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. Quote it as "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes the script output, which comes from inputs.requires and ClickHouse data, to GITHUB_OUTPUT with no sanitization: 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. A newline in the value could inject extra outputs. Clean it first with printf '%s' "$output" | tr -d '\n\r'.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes push_result to GITHUB_OUTPUT inside a fixed 'push_result<<EOF' heredoc, with no sanitization. push_result is git push output that echoes the caller-controlled STABLE_BRANCH and LATEST_VIABLE_SHA, so a value containing a newline or 'EOF' could end the block early and inject other outputs. Run the value through printf '%s' ... | tr -d '\n\r' first, and/or use a random delimiter.

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

I fixed all six findings in hardened/action/action.yml. I haven't run the action or its tests after the changes.

- **Pinned actions:** actions/setup-python is pinned to commit a26af69be951a213d495a4c3e4e4022e16d87065 (v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4). I looked up both commits rather than guessing them.
- **Script injection in the inputs:** inputs.requires is now passed through an env variable, REQUIRES, and the script uses it as "${REQUIRES}". I also quoted the path to the script (built from TEST_INFRA_PATH) and the `echo` of `output`.
- **The `latest_viable_sha` output:** line breaks are removed from the value before it is written to GITHUB_OUTPUT.
- **The `push_result` output:** the fixed `EOF` delimiter is replaced with a random one taken from /dev/urandom. Line breaks in the value become spaces, which matches what the original unquoted `echo $push_result` produced, so the output's format doesn't change.

