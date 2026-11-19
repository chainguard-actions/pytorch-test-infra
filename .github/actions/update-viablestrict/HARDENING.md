<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261118-220128** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action steps use tag refs instead of full commit SHAs: `uses: actions/setup-python@v5` (line 62) and `uses: actions/checkout@v4` (line 66).

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Step 'Get latest viable commit' breaks two rules. Rule (a): an expression is placed directly in the run script: `--required-checks "${{ inputs.requires }}"`. Anyone who controls the input can inject shell commands. Rule (b): `echo $output` is unquoted, and `output` comes from the input-influenced script result.

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Step 'Push SHA to viable/strict branch' breaks rule (b). `echo $push_result` is unquoted, and push_result holds git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values.

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

Step 'Get latest viable commit' writes `echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"`. The value comes from a script run with the untrusted inputs.requires, and it is not sanitized with `printf '%s' ... | tr -d '\n\r'` first.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

Step 'Push SHA to viable/strict branch' writes push_result to $GITHUB_OUTPUT using a fixed EOF heredoc delimiter, without sanitizing it first. push_result is git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. A value containing 'EOF' plus a newline could inject extra outputs.

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

Pinned actions/setup-python and actions/checkout to full commit SHAs, keeping the tag as a comment. Moved inputs.requires into the env var INPUT_REQUIRES and passed it double-quoted as one argument, the same as upstream's quoted expression. Quoted the script path and the echo of $output. The value written to latest_viable_sha now has newlines stripped. push_result is now written with a random delimiter from /dev/urandom and quoted inside the block. One visible change: before, the unquoted echo squashed git's output onto one line. Now the push_result output keeps git's original line breaks.

