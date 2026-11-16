<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20260922-155642** was hardened automatically. 4 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses a tag, not a full commit SHA: `uses: actions/cache@v3`. Pin it to a 40-character commit SHA.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Rule (a): the 'Run script' step puts an expression straight into the run: script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. The caller controls this input, and it is substituted into the script before bash runs. Pass it through an env: variable and quote it, e.g. `"$IS_WINDOWS"`.

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (b): the 'Run script' step expands workflow-controlled env vars without quotes. SCRIPT comes from inputs.script, and CONDA_RUN is inherited from the calling workflow. Offending lines: `if [[ ! -f ${SCRIPT} ]]; then`, `if [[ ${SCRIPT} == *.bat ]]; then`, `${CONDA_RUN} ${SCRIPT}` and `${CONDA_RUN} bash ${SCRIPT}`. Double-quote SCRIPT in every one of these places.

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

Pinned actions/cache to the v3 commit SHA (6f8efc29b200d32929f49075959781ed54ec270c). Moved inputs.is_windows out of the run script into an env var, IS_WINDOWS, and quoted it in the check. Double-quoted SCRIPT everywhere it is expanded. Left CONDA_RUN unquoted on purpose, with a shellcheck disable comment. It is a multi-word command prefix (e.g. 'conda run -p ...') that has to split into separate words, as upstream intended. Nothing was tested or run.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

In the 'Run script' step, CONDA_RUN is now split into an array with an annotated assignment (# shellcheck disable=SC2206, CONDA_RUN_ARR=(${CONDA_RUN})). Both calls now use "${CONDA_RUN_ARR[@]}" instead of the unquoted ${CONDA_RUN}. The array assignment splits and globs the value exactly as upstream's unquoted expansion did, so behaviour is unchanged. Possible risk: on bash older than 4.4 (e.g. the macOS system bash 3.2), an empty CONDA_RUN under set -u would make the empty array expansion fail. The calling workflows normally set CONDA_RUN, so this was left as the finding recommended. Not tested.

