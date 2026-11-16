<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261029-163400** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite steps reference actions by mutable tag instead of a 40-char commit SHA: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression straight into the run script: '--required-checks "${{ inputs.requires }}" \'. Because the input is substituted into the script text before bash runs, a value containing quotes or $(...) can run commands. Rule (b): the step also expands '$output', which comes from that input, without quotes: 'echo $output'. Fix: move inputs.requires into an env: variable and use "$REQUIRES", and quote "$output".

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Rule (b): in the 'Push SHA to viable/strict branch' step, '$push_result' is expanded without quotes: 'echo $push_result'. It holds git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. Quote it as "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

In the 'Get latest viable commit' step, '$output' is written to GITHUB_OUTPUT with 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' and is not cleaned first with printf '%s' ... | tr -d '\n\r'. The value comes from a script whose arguments and data come from inputs (requires, clickhouse-*), so newlines in it could inject extra outputs.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

In the 'Push SHA to viable/strict branch' step, '$push_result' is written to GITHUB_OUTPUT through a fixed 'EOF' heredoc delimiter and is not cleaned first with printf '%s' ... | tr -d '\n\r'. It holds git output built from the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values, so it could end the delimiter early or inject extra outputs.

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

All changes are in action.yml. I haven't run the action to test these changes.

- **unpinned-uses:** `actions/setup-python` and `actions/checkout` now point to full commit SHAs, looked up with lookup_action_sha. The original tag is kept as a comment after each one.
- **script-injection / static-inline-injection:** `inputs.requires` moved into the step's `env:` as REQUIRES and is passed to the script as "$REQUIRES". `$output` and `$push_result` are now quoted when echoed, and so is the script path.
- **github-env-injection:** newlines and carriage returns are removed from `latest_viable_sha` (with `printf '%s' | tr -d '\n\r'`) before it is written to GITHUB_OUTPUT. `push_result` now uses a heredoc delimiter that is random on every run (16 bytes from /dev/urandom) instead of the fixed 'EOF'.

One behaviour change: upstream's unquoted `echo $push_result` joined git's multi-line output onto one line. Because it is now quoted, the `push_result` output keeps git's original line breaks.

