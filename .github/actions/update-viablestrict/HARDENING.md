<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261123-205410** was hardened automatically. 5 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps use mutable tag refs rather than full 40-character commit SHAs: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression straight into the run script: '--required-checks "${{ inputs.requires }}" \'. The caller controls inputs.requires, and the value is substituted into the script before bash runs it. Move it into an env: variable such as REQUIRES and use "$REQUIRES".

Locations:

- `action.yml:94`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' with no sanitization. $output is the output of a script driven by the untrusted inputs.requires value and by external ClickHouse data. A newline in it could inject extra step outputs. Run printf '%s' "$output" | tr -d '\n\r' just before the write.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes $push_result to $GITHUB_OUTPUT inside a fixed 'EOF' heredoc delimiter, with no sanitization. push_result is git push output, which can echo back the caller-controlled STABLE_BRANCH (inputs.stable-branch) and LATEST_VIABLE_SHA values. A value containing a newline followed by 'EOF' could end the block early and inject arbitrary outputs. Run printf '%s' ... | tr -d '\n\r' on the value first, or use a random delimiter.

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

Pinned actions/setup-python to a26af69b… # v5 and actions/checkout to 11d5960a… # v4. Moved the inputs.requires expression into env as REQUIRES and replaced it with "$REQUIRES" in the script. The fetch output is captured on its own line first, so set -e still stops the step if the script fails, then newlines are stripped before writing latest_viable_sha. The push_result block now uses a random delimiter read from /dev/urandom in place of the fixed EOF; the value is written the same way upstream wrote it.

### Iteration 2

**Fixes applied:** github-env-injection, script-injection

**Notes:**

In action.yml, the 'Push SHA to viable/strict branch' step now cleans push_result before writing it to GITHUB_OUTPUT. It turns runs of whitespace into single spaces and trims the ends, matching what upstream's unquoted echo printed, then strips newlines with tr -d '\n\r'. The value goes into the existing heredoc as a quoted "$safe_push_result", and the random delimiter is unchanged.

