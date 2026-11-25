<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261125-022556** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses an action by tag instead of a full 40-character commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Rule (a): an expression is placed straight into the 'Run script' run: block: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. The value of inputs.is_windows is pasted into the script text before bash runs, so a crafted input can run its own commands. Rule (b): the env var SCRIPT (set from inputs.script) and the inherited env var CONDA_RUN are expanded without quotes: `if [[ ! -f ${SCRIPT} ]]`, `if [[ ${SCRIPT} == *.bat ]]`, `${CONDA_RUN} ${SCRIPT}` and `${CONDA_RUN} bash ${SCRIPT}`. Move is_windows into env and put double quotes around every expansion.

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

Pinned actions/cache to 6f8efc29b200d32929f49075959781ed54ec270c (v3). Moved inputs.is_windows into env IS_WINDOWS and quoted it. Quoted every SCRIPT expansion. CONDA_RUN is a command prefix, so it now goes into a bash array assigned unquoted (same whitespace split as upstream's unquoted ${CONDA_RUN}) and is expanded as ${conda_run[@]+"${conda_run[@]}"}. That form is safe under set -u even on bash 3.2 when the array is empty.

