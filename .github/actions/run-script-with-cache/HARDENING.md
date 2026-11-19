<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261118-220128** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite step uses a mutable tag rather than a full 40-char commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Rule (a): the 'Run script' step interpolates an expression directly inside the run: script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. Move it to an env var (e.g. IS_WINDOWS) and reference it as "$IS_WINDOWS". Rule (b): the env var SCRIPT (from inputs.script) is expanded unquoted in several places: `if [[ ! -f ${SCRIPT} ]]` (line 56), `if [[ ${SCRIPT} == *.bat ]]` (line 60), `${CONDA_RUN} ${SCRIPT}` (line 61), `${CONDA_RUN} bash ${SCRIPT}` (line 63). Each of these should be written as "${SCRIPT}".

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

Pinned actions/cache@v3 to its commit SHA 6f8efc29b200d32929f49075959781ed54ec270c, keeping a '# v3' comment. Moved inputs.is_windows out of the run: script into an env var (IS_WINDOWS), which the script now reads as "${IS_WINDOWS}". Put double quotes around every expansion of ${SCRIPT}, since the script input is a single file path. Left ${CONDA_RUN} unquoted as upstream has it: it comes from BUILD_ENV_FILE and may be several words that need splitting. Nothing was run to test these changes.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

In the 'Run script' step, CONDA_RUN is now assigned to a bash array using an unquoted assignment, `CONDA_RUN_ARR=(${CONDA_RUN})`. This splits and globs the value exactly like upstream's unquoted expansion did, so the conda wrapper (for example 'conda run -p ...') behaves the same. The command then runs through the quoted array expansion. The `${arr[@]+...}` guard keeps an empty CONDA_RUN from failing under set -u on older bash. The script path stays double-quoted.

