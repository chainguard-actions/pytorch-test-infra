<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261029-163400** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step references an action by mutable tag instead of a full commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Step 'Run script' breaks rule (a), direct expression interpolation. Its run: block puts an input expression straight into the shell script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. Move it into an env: variable and expand it double-quoted. The same step also breaks rule (b): workflow-controlled env vars are expanded without quotes. These are `if [[ ! -f ${SCRIPT} ]]` (line 56), `if [[ ${SCRIPT} == *.bat ]]` (line 60), `${CONDA_RUN} ${SCRIPT}` (line 61) and `${CONDA_RUN} bash ${SCRIPT}` (line 63). SCRIPT comes from inputs.script. CONDA_RUN is inherited from the calling workflow's environment.

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

I fixed all three findings in action.yml.

- **unpinned-uses:** `actions/cache@v3` now points to the full commit SHA I looked up: `@6f8efc29b200d32929f49075959781ed54ec270c # v3`.
- **script-injection / static-inline-injection:** `inputs.is_windows` no longer appears inline in the script. It is passed in through a new `IS_WINDOWS` env variable and compared with double quotes. `SCRIPT` is now double-quoted everywhere it is used.
- **CONDA_RUN:** this is a command prefix (e.g. `conda run -p ...`), so it has to split into separate words the way upstream's unquoted `${CONDA_RUN}` did. It is now split into an array with `conda_run=(${CONDA_RUN})` (same whitespace split and globbing as upstream). The array is expanded as `${conda_run[@]+"${conda_run[@]}"}`, so an empty `CONDA_RUN` adds nothing to the command and doesn't trip `set -u` on older bash. As before, an unset `CONDA_RUN` still stops the step when `set -u` is on.

I didn't run the action or any tests after these changes.

