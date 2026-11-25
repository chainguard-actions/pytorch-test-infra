<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261125-022556** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps reference actions by mutable tag instead of a 40-char commit SHA: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66).

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Step 'Get latest viable commit': rule (a) violated. The expression is interpolated straight into the run script: '--required-checks "${{ inputs.requires }}"'. A crafted 'requires' input can break out of the quotes and run arbitrary commands. Rule (b) also applies: the command output is expanded without quotes in 'echo $output', and the path is unquoted in 'python ${TEST_INFRA_PATH}/tools/scripts/fetch_latest_green_commit.py'. Fix: pass inputs.requires through an env var and double-quote every expansion.

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Step 'Push SHA to viable/strict branch': rule (b) violated. 'echo $push_result' expands without quotes a value built from git output, and that output includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA env vars (from inputs.stable-branch and steps.get-latest-commit.outputs). Fix: quote it as "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

Step 'Get latest viable commit': 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' writes script output to GITHUB_OUTPUT without first running it through printf '%s' ... | tr -d '\n\r'. That output comes from a script run with the untrusted inputs.requires value, so injected newlines could create extra outputs.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

Step 'Push SHA to viable/strict branch': push_result is written to GITHUB_OUTPUT through a fixed 'EOF' heredoc delimiter without sanitizing it first. push_result holds git push output, which echoes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. If that text contains a line reading 'EOF' plus newlines, it can end the heredoc early and inject extra outputs. Fix: run it through printf '%s' | tr -d '\n\r' (or use a random delimiter) before the write.

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

Pinned actions/setup-python (v5) and actions/checkout (v4) to full commit SHAs. Moved inputs.requires into the env var INPUT_REQUIRES and quoted the script path and $output. latest_viable_sha now has newlines stripped before it is written to GITHUB_OUTPUT. push_result is now written quoted between a random delimiter read from /dev/urandom, replacing the fixed EOF. The value is kept multi-line, so the output can now contain newlines where upstream's unquoted echo joined the lines with spaces. Nothing was run to test these changes.

