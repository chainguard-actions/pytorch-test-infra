<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261109-232755** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

These composite action steps point to mutable version tags instead of full 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66). Pin each one to a commit SHA, for example actions/checkout@<sha> # v4.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): in step 'Get latest viable commit', the expression ${{ inputs.requires }} is placed straight into the run: script: '--required-checks "${{ inputs.requires }}" \'. The template is substituted before the shell runs, so a value containing quotes or $(...) can run commands. Move it into an env: variable (e.g. REQUIRES: ${{ inputs.requires }}) and use "$REQUIRES" in the script. The same step also expands $output without quotes in 'echo $output' (line 98). That value is derived from the input-driven script output, so quote it as "$output".

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Rule (b): in step 'Push SHA to viable/strict branch', 'echo $push_result' (line 119) expands $push_result without quotes. That variable holds git push output, which includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. Quote it: echo "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

Step 'Get latest viable commit' writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' with no sanitization first. $output comes from a script run with the untrusted inputs.requires value and with data fetched from ClickHouse. A newline in it could inject extra outputs. Before the write, run safe=$(printf '%s' "$output" | tr -d '\n\r') and write $safe instead.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

Step 'Push SHA to viable/strict branch' writes $push_result to $GITHUB_OUTPUT through a fixed 'push_result<<EOF' heredoc, with no sanitization first (lines 117-121). $push_result is git push output that echoes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA. If that output contains an 'EOF' line, it can end the heredoc early and inject other outputs. Remove newlines with printf '%s' "$push_result" | tr -d '\n\r' before the write, or use a random delimiter.

Locations:

- `action.yml:121`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python and actions/checkout to commit SHAs. Moved inputs.requires into env REQUIRES. Quoted the $output and $push_result echoes and the script path. latest_viable_sha now has newlines and carriage returns stripped before it is written to GITHUB_OUTPUT. The push_result heredoc now uses a delimiter drawn from /dev/urandom on each run instead of the fixed EOF. One behaviour change: because the echo is now quoted, push_result can span several lines. Upstream's unquoted echo collapsed it onto one line.

