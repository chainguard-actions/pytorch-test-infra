<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261021-234439** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action pins its actions to version tags instead of 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66).

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression straight into the run script: '--required-checks "${{ inputs.requires }}" \'. The template value is substituted before the shell parses the script, so a '"' or '$(...)' in the input runs as a command. Move it into an env var (e.g. REQUIRES) and use "$REQUIRES". Rule (b): the same step also expands workflow-derived data without quotes: 'python ${TEST_INFRA_PATH}/tools/scripts/fetch_latest_green_commit.py' and 'echo $output', where $output is built from the inputs.

Locations:

- `action.yml:94`
- `action.yml:93`
- `action.yml:98`

### script-injection (severity: high)

Rule (b): the 'Push SHA to viable/strict branch' step runs 'echo $push_result' without quotes. $push_result holds git push output, which includes the input-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. Quote it: "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output comes from a script run with the untrusted inputs.requires value, and it is written without the printf '%s' ... | tr -d '\n\r' sanitization step.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes $push_result to $GITHUB_OUTPUT through a heredoc ('echo push_result<<EOF' / 'echo $push_result' / 'echo EOF' >> "${GITHUB_OUTPUT}"). push_result is git output that contains the input-derived STABLE_BRANCH and LATEST_VIABLE_SHA values. Nothing is sanitized, so a value containing 'EOF' plus a newline can inject extra outputs.

Locations:

- `action.yml:116`
- `action.yml:121`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python and actions/checkout to their full commit SHAs, with the tag kept in a comment. Moved inputs.requires out of the run script and into an env var (REQUIRES), and quoted the script path and the echo of $output and $push_result. The latest_viable_sha value now has newlines stripped (printf | tr -d '\n\r') before it is written to GITHUB_OUTPUT. The push_result heredoc now uses a random delimiter from /dev/urandom instead of a fixed 'EOF', so a line in the value can no longer end the block early. One change you might notice: because $push_result is now quoted, the push_result output keeps git's line breaks, where upstream's unquoted echo joined everything onto one line.

