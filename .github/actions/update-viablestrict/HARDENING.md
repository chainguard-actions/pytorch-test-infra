<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261021-234439** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action uses tag refs instead of full 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66).

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression directly into the run: script: '--required-checks "${{ inputs.requires }}"'. The input is substituted into the script text before bash parses it, so a crafted value can break out of the quotes and run commands. Move it into an env: variable (e.g. REQUIRES) and use "$REQUIRES".

Locations:

- `action.yml:94`

### script-injection (severity: high)

Rule (b): the 'Push SHA to viable/strict branch' step runs 'echo $push_result' unquoted. push_result holds git output that includes the workflow-controlled STABLE_BRANCH (inputs.stable-branch) and LATEST_VIABLE_SHA values. Use "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' without the printf '%s' | tr -d '\n\r' step first. $output comes from a script that is called with the untrusted inputs.requires value and with ClickHouse data, so a newline in it could inject extra outputs.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes push_result to $GITHUB_OUTPUT through a heredoc ('echo push_result<<EOF' / 'echo $push_result' / 'echo EOF'). push_result is git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values, and it is not sanitized before the write. A value containing the EOF delimiter on its own line could inject more outputs.

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

Pinned actions/setup-python and actions/checkout to full commit SHAs. Moved inputs.requires into env (REQUIRES) and pass it as "$REQUIRES". latest_viable_sha is now written to GITHUB_OUTPUT after newline stripping, and the command substitution stays a bare assignment so errexit still applies. push_result is now quoted and written with a random per-run heredoc delimiter from /dev/urandom.

