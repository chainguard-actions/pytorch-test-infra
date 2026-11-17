<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261029-163400** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps use mutable tag refs instead of full 40-char commit SHAs: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66).

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Step 'Get latest viable commit': rule (a) is broken. The run script puts an expression straight into the shell command: '--required-checks "${{ inputs.requires }}" \'. Because the input is substituted into the script text before bash runs, an attacker-controlled value can break out of the quotes and run its own commands. Fix: move it into an env var (e.g. REQUIRES: ${{ inputs.requires }}) and use "$REQUIRES". Rule (b) is also broken: 'echo $output' (line 98) leaves unquoted a value built from the workflow-controlled requires input.

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Step 'Push SHA to viable/strict branch': rule (b) is broken. 'echo $push_result' leaves unquoted the git push output, and that output includes the input-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. Fix: quote it as "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

Step 'Get latest viable commit' writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output comes from a script that is driven by inputs.requires, and it is not passed through printf '%s' ... | tr -d '\n\r' before the write. Embedded newlines could inject extra step outputs.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

Step 'Push SHA to viable/strict branch' writes push_result to $GITHUB_OUTPUT using a heredoc with a fixed 'EOF' delimiter: echo 'push_result<<EOF'; echo $push_result; echo EOF } >> "${GITHUB_OUTPUT}". push_result is git output that includes the input-controlled STABLE_BRANCH and LATEST_VIABLE_SHA, and it is not sanitized with printf '%s' ... | tr -d '\n\r'. A value containing a newline followed by 'EOF' could end the heredoc early and inject extra outputs.

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

Pinned actions/setup-python and actions/checkout to full commit SHAs. Moved inputs.requires into the REQUIRES env var and quoted it where it is used. The Python script path and the echo of output and push_result are now quoted. The latest_viable_sha output now has newlines stripped before it is written. The fixed EOF delimiter for push_result is now a random one generated from /dev/urandom, and the multi-line value is written as is. One behaviour change: push_result used to be written unquoted, which squashed git's output onto one line. Now it keeps its original line breaks.

