<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261119-192116** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that use mutable tags instead of full commit SHAs: line 62 'uses: actions/setup-python@v5' and line 66 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression straight into the run script: '--required-checks "${{ inputs.requires }}" \'. The value of inputs.requires is pasted into the bash script before the shell runs, so a quote or $(...) in it gets executed. Move it into an env var (e.g. REQUIRES) and use "$REQUIRES". The same step also has unquoted expansions on line 93 (python ${TEST_INFRA_PATH}/...) and line 98 (echo $output).

Locations:

- `action.yml:94`

### script-injection (severity: high)

Rule (b): the 'Push SHA to viable/strict branch' step expands push_result without quotes: 'echo $push_result'. push_result holds git push output, which repeats the workflow-controlled values STABLE_BRANCH (inputs.stable-branch) and LATEST_VIABLE_SHA (a step output). The unquoted expansion splits words and expands globs on that data. Quote it: echo "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output comes from a script run with the untrusted inputs.requires value, and it is written without the printf '%s' ... | tr -d '\n\r' step first. A newline in it could add extra step outputs.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes push_result (git push output that includes inputs.stable-branch and the LATEST_VIABLE_SHA step output) into $GITHUB_OUTPUT inside a fixed 'EOF' heredoc (lines 117-121). It is not passed through printf '%s' ... | tr -d '\n\r' first, so the value could close the delimiter early or inject extra outputs.

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

All six findings are fixed, all in action.yml. Nothing was run or tested after the edits.

- **Pinned actions:** actions/setup-python is now pinned to commit a26af69b… (tag v5) and actions/checkout to commit 11d5960a… (tag v4). Both SHAs came from lookup_action_sha.
- **inputs.requires in the run script:** it now goes through a REQUIRES env var and is used as "$REQUIRES". The script path and the `echo "$output"` line are now quoted too.
- **latest_viable_sha output:** line breaks are removed with `printf '%s' | tr -d '\n\r'` before the value is written to $GITHUB_OUTPUT. The step still stops if the Python script fails.
- **push_result output:** `echo $push_result` is now quoted. The fixed 'EOF' end marker is replaced with a random one drawn from /dev/urandom, so the git output can't close the block early or add extra outputs.

One behaviour change: because push_result is now quoted, it keeps git's line breaks. Before, the unquoted echo squashed it onto one line, so anything reading this output will now get several lines.

