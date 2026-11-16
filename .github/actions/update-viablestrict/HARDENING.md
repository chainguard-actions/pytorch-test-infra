<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261109-232755** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses mutable tag refs instead of full 40-char commit SHAs: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts a GitHub expression straight into the run: script: '--required-checks "${{ inputs.requires }}" \'. The caller controls inputs.requires, and the value is substituted into the script text before the shell parses it, so it can break out of the quotes and run commands. Pass it in through an env: variable (e.g. REQUIRES) and use "$REQUIRES" instead.

Locations:

- `action.yml:94`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' without sanitizing it first. $output comes from a script run with the untrusted inputs.requires value and ClickHouse data. If it contains a newline, it can inject extra step outputs. Apply printf '%s' "$output" | tr -d '\n\r' before the write.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes push_result to $GITHUB_OUTPUT using a heredoc with a fixed delimiter: 'echo push_result<<EOF', 'echo $push_result', 'EOF'. push_result is git output that includes the input-derived STABLE_BRANCH and LATEST_VIABLE_SHA values. It is not sanitized, so a value containing an 'EOF' line can end the heredoc early and inject arbitrary outputs. Sanitize with printf '%s' ... | tr -d '\n\r', or use a random delimiter.

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

Pinned actions/setup-python and actions/checkout to full commit SHAs, keeping the version tag as a comment. Moved inputs.requires into the env var REQUIRES, so the script no longer contains the expression. The output written to latest_viable_sha now has newlines removed first. The push_result heredoc now uses a random delimiter read from /dev/urandom instead of a fixed 'EOF', and the value it writes is unchanged from upstream. Nothing was run or tested after these edits.

