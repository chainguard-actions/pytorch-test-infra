<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261109-192709** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step uses a mutable tag instead of a full 40-char commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Step 'Run script' violates rule (a): a GitHub Actions expression is placed directly in the run script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. The value of inputs.is_windows is pasted into the script before bash runs, so it can inject commands. Move it into an env var (e.g. IS_WINDOWS: ${{ inputs.is_windows }}) and use "$IS_WINDOWS". The same step also violates rule (b): the workflow-controlled env vars SCRIPT (from inputs.script) and CONDA_RUN (inherited from the calling workflow) are expanded without quotes: `if [[ ! -f ${SCRIPT} ]]` (line 56), `if [[ ${SCRIPT} == *.bat ]]` (line 60), `${CONDA_RUN} ${SCRIPT}` (line 61), `${CONDA_RUN} bash ${SCRIPT}` (line 63). Quote them, e.g. "$SCRIPT".

Locations:

- `action.yml:51`
- `action.yml:56`
- `action.yml:60`
- `action.yml:61`
- `action.yml:63`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.is_windows }}" appears directly in run: block of step "Run script"; move to env: map

Locations:

- `action.yml:51`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

I pinned actions/cache@v3 to its full commit SHA, 6f8efc29b200d32929f49075959781ed54ec270c, and kept '# v3' as a comment.

I moved inputs.is_windows out of the run script into an IS_WINDOWS environment variable, and SCRIPT is now quoted everywhere it is used.

I did not simply quote CONDA_RUN, though the finding suggests it. It holds a command prefix such as 'conda run -p <env>', and quoting it would pass that as one word, so the command would break. Instead it goes into a bash array assigned unquoted, which splits it the same way upstream's unquoted expansion did. The array is expanded with the ${arr[@]+"${arr[@]}"} pattern, so an empty or unset CONDA_RUN does not trigger set -u's unbound-variable error in older bash 3.2 (macOS runners). Splitting a variable this way does not run anything inside its value, so it is not an injection risk.

Nothing was run or tested after these edits.

