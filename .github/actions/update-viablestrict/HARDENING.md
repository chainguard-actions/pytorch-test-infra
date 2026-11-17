<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261103-202628** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite steps reference actions by mutable tag rather than a full 40-char commit SHA: line 62 'uses: actions/setup-python@v5' and line 66 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression straight into the run script: '--required-checks "${{ inputs.requires }}" \'. The input value is substituted into the bash script before the shell runs, so a value containing a quote or $(...) can run arbitrary commands. Fix: move it to env (e.g. REQUIRES: ${{ inputs.requires }}) and use "$REQUIRES".

Locations:

- `action.yml:94`

### script-injection (severity: high)

Rule (b): the 'Push SHA to viable/strict branch' step expands push_result unquoted: 'echo $push_result'. push_result holds git push output, which repeats the workflow-controlled STABLE_BRANCH (inputs.stable-branch) and LATEST_VIABLE_SHA (step output) values. Unquoted, the value is word-split and glob-expanded. Use "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' with no sanitization first. $output is the stdout of a script driven by the untrusted inputs.requires value and by ClickHouse data (from inputs.clickhouse-url). A newline in it could inject extra step outputs. Strip newlines with printf '%s' "$output" | tr -d '\n\r' before the write.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes push_result to $GITHUB_OUTPUT inside a fixed 'push_result<<EOF' heredoc block (lines 117-121) with no sanitization first. push_result is git push output that repeats the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. Text containing a line 'EOF' plus newlines could end the block early and inject arbitrary outputs. Sanitize with printf '%s' ... | tr -d '\n\r' or use a random delimiter.

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

All the fixes are in action.yml. I haven't run the action or any tests after the changes.

- **Pinned actions:** actions/setup-python is now pinned to commit a26af69b… (was v5) and actions/checkout to 11d5960a… (was v4). Each line keeps the tag as a comment so it's still readable.
- **`inputs.requires` moved out of the script:** the value now goes in through a `REQUIRES` env var and is passed as "$REQUIRES". The path to the Python script is now quoted too.
- **`latest_viable_sha` output:** newlines are now removed from the value before it is written to $GITHUB_OUTPUT. `echo $output` is now quoted.
- **`push_result` output:** the fixed `EOF` heredoc end marker is replaced by a random one read from /dev/urandom each run, so output text can't close the block early. `$push_result` is now quoted, as the finding asked.

One behaviour change from that quoting: upstream's unquoted `echo` joined the git push output onto a single line. The `push_result` output now keeps git's original line breaks.

