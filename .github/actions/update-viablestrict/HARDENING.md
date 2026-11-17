<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261112-155209** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action references actions by a mutable tag instead of a full 40-character commit SHA: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Sub-rule (a): a GitHub expression is placed straight into a run: script in the 'Get latest viable commit' step: '--required-checks "${{ inputs.requires }}" \'. The value is pasted into the script text before the shell runs, so an attacker-controlled 'requires' value can break out of the quotes and run commands. Fix: pass it through an env: variable (e.g. REQUIRES: ${{ inputs.requires }}) and use "$REQUIRES".

Locations:

- `action.yml:94`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' with no sanitization. $output is the result of a script that receives inputs.requires and ClickHouse inputs, so it comes from untrusted input. Newlines in it could add extra outputs. Fix: run printf '%s' "$output" | tr -d '\n\r' just before the write.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes $push_result to $GITHUB_OUTPUT inside a fixed 'push_result<<EOF' heredoc ('echo $push_result' at line 119). push_result is git push output, and that output includes STABLE_BRANCH (inputs.stable-branch) and LATEST_VIABLE_SHA (a step output). It is not sanitized and the delimiter is predictable, so a crafted value can end the heredoc early and add arbitrary outputs. Fix: sanitize with printf '%s' "$push_result" | tr -d '\n\r' before the write, or use a random delimiter.

Locations:

- `action.yml:119`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python and actions/checkout to full commit SHAs, keeping the tag in a comment. Moved inputs.requires into env as REQUIRES and passed it double-quoted. latest_viable_sha now has newlines stripped before it is written. The push_result value now has newlines stripped too, and is written inside a heredoc whose delimiter is random on every run (from /dev/urandom). Side effect: upstream's unquoted echo turned newlines in push_result into spaces, but the new version removes them, so adjacent lines now run together.

