<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261123-205410** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses a mutable tag instead of a full 40-character commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Rule (a): the 'Run script' step puts an expression straight into the run: script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. Pass inputs.is_windows in through an env: variable and quote it, e.g. `"$IS_WINDOWS"`.

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (b): the 'Run script' step expands workflow-controlled variables without quotes. SCRIPT comes from inputs.script, and CONDA_RUN is inherited from the calling workflow's environment. Offending lines: `if [[ ! -f ${SCRIPT} ]]; then`, `if [[ ${SCRIPT} == *.bat ]]; then`, `${CONDA_RUN} ${SCRIPT}`, `${CONDA_RUN} bash ${SCRIPT}`. Quote these expansions ("$SCRIPT").

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

I fixed all four findings in action.yml; nothing has been run to test the changes.

- **Unpinned action:** `actions/cache@v3` is now pinned to its full commit SHA, `6f8efc29b200d32929f49075959781ed54ec270c # v3`.
- **Inline expression:** `inputs.is_windows` is no longer written straight into the script. It is passed in as the env variable `IS_WINDOWS` and the check now reads `"$IS_WINDOWS"`.
- **Unquoted variables:** every use of `SCRIPT` is now quoted.
- **`CONDA_RUN`:** this holds a multi-word command prefix (something like `conda run -p <env>`), so quoting it as one word would break the command. Instead I split it into a bash array with `conda_run=(${CONDA_RUN:-})`, which splits it exactly as upstream's unquoted `${CONDA_RUN}` did. The array is run with `${conda_run[@]+"${conda_run[@]}"}`, so an empty or unset `CONDA_RUN` still works under `set -u`, even on older bash. Like upstream's version, the split does not evaluate anything in the value.

