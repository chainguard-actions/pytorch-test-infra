<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261109-232755** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references an action by a mutable tag instead of a full 40-character commit SHA: 'uses: actions/cache@v3'.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Step 'Run script' breaks both rules. (a) An expression is placed directly in the run script: 'if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then'. The input is pasted into the script before bash runs, so a crafted value can run commands. (b) The env var SCRIPT, which comes from inputs.script, is expanded without quotes: 'if [[ ! -f ${SCRIPT} ]]', 'if [[ ${SCRIPT} == *.bat ]]', '${CONDA_RUN} ${SCRIPT}' and '${CONDA_RUN} bash ${SCRIPT}'. The inherited env var CONDA_RUN, which the calling workflow controls, is also expanded without quotes. Fix: move inputs.is_windows into an env var and quote it ("$IS_WINDOWS"), and quote every expansion of SCRIPT ("$SCRIPT").

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

I made three changes to action.yml. 1) Pinned actions/cache to its full commit SHA, 6f8efc29b200d32929f49075959781ed54ec270c, with a '# v3' comment. 2) Moved inputs.is_windows out of the run script into an env var, IS_WINDOWS, and quoted it where it is checked ("$IS_WINDOWS"). 3) Quoted every use of SCRIPT ("$SCRIPT"). CONDA_RUN holds a command prefix such as 'conda run -p <env>', so it has to split into several words the way upstream's unquoted expansion did. It is now split into a bash array with an unquoted assignment and expanded as ${conda_run[@]+"${conda_run[@]}"}. That form still works when CONDA_RUN is empty under 'set -u', including on older bash. Nothing was run or tested.

