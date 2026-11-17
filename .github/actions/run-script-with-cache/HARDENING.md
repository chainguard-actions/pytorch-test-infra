<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step pins its action to a mutable tag, not a 40-character commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Rule (a) is violated in the 'Run script' step. An expression is put straight into the run script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. Whoever calls the action controls inputs.is_windows, so they can inject shell code. Move it into an env: variable and quote it, e.g. "$IS_WINDOWS".

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (b) is violated in the 'Run script' step. The env var SCRIPT (from inputs.script) is expanded without double quotes in several places: `if [[ ! -f ${SCRIPT} ]]`, `echo "...(${SCRIPT})..."` (this one is inside quotes), `if [[ ${SCRIPT} == *.bat ]]`, `${CONDA_RUN} ${SCRIPT}` and `${CONDA_RUN} bash ${SCRIPT}`. The command-argument uses are split on whitespace and glob-expanded, so they need double quotes ("$SCRIPT"). CONDA_RUN is also inherited from the calling workflow and expanded without quotes.

Locations:

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

I fixed all three findings in action.yml. Nothing was run or tested.

- **Pinned the cache action:** `actions/cache` now points to commit `6f8efc29b200d32929f49075959781ed54ec270c` instead of the `v3` tag. I looked the SHA up for `v3` and kept the tag name as a comment.
- **Removed the inline expression:** `inputs.is_windows` is now passed in through the step's `env:` block as `IS_WINDOWS` and compared quoted, so it is no longer written straight into the script.
- **Quoted `SCRIPT`:** every place `SCRIPT` is used as a command argument or tested is now in double quotes.
- **Changed how `CONDA_RUN` is used:** it is a command prefix (like `conda run -p ...`) that can hold several words. Wrapping it in quotes would turn it into one word, so instead I split it into a list (`conda_run=(${CONDA_RUN})`) and run `"${conda_run[@]}"`. This splits it on spaces exactly as upstream did, and nothing inside it is executed as code.

