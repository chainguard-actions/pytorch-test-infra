<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261027-001733** was hardened automatically. 5 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that pin actions by tag instead of a full 40-character commit SHA: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66).

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression straight into its run script: '--required-checks "${{ inputs.requires }}" \'. The value is substituted into the script text before bash parses it, so a crafted 'requires' input (for example one containing a double quote or $(...)) can run arbitrary commands. Fix: move it into an env: variable (e.g. REQUIRES: ${{ inputs.requires }}) and pass it as "$REQUIRES".

Locations:

- `action.yml:94`

### github-env-injection (severity: high)

The 'Get latest viable commit' step runs 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output is the result of a script whose arguments come from inputs.requires, and it is written without the sanitization step (printf '%s' "$output" | tr -d '\n\r'). A newline in the value could inject extra step outputs.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes push_result to $GITHUB_OUTPUT in a fixed heredoc ('echo push_result<<EOF' / 'echo $push_result' / 'echo EOF'), with no printf '%s' | tr -d '\n\r' first. push_result holds git push output, which includes the untrusted STABLE_BRANCH (inputs.stable-branch) and LATEST_VIABLE_SHA (steps.*.outputs). If that output contains a line reading 'EOF', it can end the heredoc early and add arbitrary outputs. The expansion is also unquoted.

Locations:

- `action.yml:116`
- `action.yml:118`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python and actions/checkout to full commit SHAs. Moved inputs.requires into env REQUIRES and passed it quoted. latest_viable_sha is now stripped of newlines before it is written to GITHUB_OUTPUT. The push_result heredoc now uses a random delimiter read from /dev/urandom. The value is still collapsed to single-space-separated words as upstream's unquoted echo did, but with globbing disabled, and it is printed quoted.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

In action.yml, the 'Get latest viable commit' step had `echo $output` unquoted. It is now `echo "$output"`, so the shell no longer splits the value into words or expands glob characters in it. This only affects the log line, since the GITHUB_OUTPUT write already used the newline-stripped copy, so the action's outputs don't change. Nothing was run to test this.

