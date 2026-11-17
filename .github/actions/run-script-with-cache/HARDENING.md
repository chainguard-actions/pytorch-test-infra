<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20260922-155642** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references an action by a mutable tag instead of a full 40-character commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Step 'Run script' breaks both sub-rules. (a) The expression is placed directly in the run script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. Pass inputs.is_windows through an env var and quote it. (b) Workflow-controlled env vars are expanded without quotes: `if [[ ! -f ${SCRIPT} ]]`, `if [[ ${SCRIPT} == *.bat ]]`, `${CONDA_RUN} ${SCRIPT}` and `${CONDA_RUN} bash ${SCRIPT}`. SCRIPT comes from inputs.script. CONDA_RUN is inherited from the calling workflow. Both must be double-quoted.

Locations:

- `action.yml:51`
- `action.yml:56`
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

I fixed all three findings in action.yml. 1) Pinned actions/cache@v3 to its full commit SHA, 6f8efc29b200d32929f49075959781ed54ec270c (# v3). 2) Moved inputs.is_windows into an env var (IS_WINDOWS) and quoted it in the test. 3) Double-quoted SCRIPT everywhere it is used. 4) Did not wrap CONDA_RUN in quotes as the finding asked, because that would break it. It holds a command plus its arguments (like `conda run -p <env>`), and upstream depends on the shell splitting it into separate words. Quoting it would turn the whole thing into one argument, and the step would then try to run a program with that full string as its name. Instead it is split into a bash array the same way upstream's unquoted expansion did, then expanded as ${conda_run[@]+"${conda_run[@]}"}. That form means an empty CONDA_RUN adds no arguments and doesn't trip `set -u` on older bash. An unquoted split like this doesn't run anything inside the value, so it isn't an injection risk. Nothing was run or tested.

