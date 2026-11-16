<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses a mutable tag instead of a full 40-character commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Rule (a): the 'Run script' step puts a GitHub Actions expression directly into the run: script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. The value of inputs.is_windows is pasted into the bash script before it runs, so an attacker can inject commands. Move it into an env: variable (e.g. IS_WINDOWS) and reference it as "$IS_WINDOWS".

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (b): in the 'Run script' step, the env var SCRIPT (from inputs.script) and the inherited env var CONDA_RUN are expanded without quotes: `if [[ ! -f ${SCRIPT} ]]`, `${CONDA_RUN} ${SCRIPT}` and `${CONDA_RUN} bash ${SCRIPT}`. Expansions of workflow-controlled data must be double-quoted (e.g. "${SCRIPT}").

Locations:

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

I pinned actions/cache to its full commit SHA, 6f8efc29b200d32929f49075959781ed54ec270c (# v3). I moved inputs.is_windows out of the run: script into an env variable, IS_WINDOWS, and the script now reads it as "$IS_WINDOWS". SCRIPT is now double-quoted everywhere it is used. I did not double-quote CONDA_RUN, even though the finding asks for it. It holds a command prefix such as 'conda run -p ...', and quoting it would pass that whole prefix as one argument, which would break the step. Instead it is split into an array with the same whitespace splitting as upstream's unquoted ${CONDA_RUN}. The array is then expanded quoted, using a form that still works under set -u when CONDA_RUN is empty. This splitting does not run anything inside the value, so it is not an injection risk. Nothing was run or tested; these are edits to action.yml only.

