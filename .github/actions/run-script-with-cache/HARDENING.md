<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261109-192709** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references an action by a mutable tag instead of a 40-character commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Rule (a): the 'Run script' step puts a GitHub expression straight into the run script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. The input should go into an env var (e.g. IS_WINDOWS) and be referenced as "$IS_WINDOWS".

Locations:

- `action.yml:51`

### script-injection (severity: high)

Rule (b): in the 'Run script' step, the env var SCRIPT (set from inputs.script) and the inherited env var CONDA_RUN are expanded without double quotes: `if [[ ! -f ${SCRIPT} ]]`, `if [[ ${SCRIPT} == *.bat ]]`, `${CONDA_RUN} ${SCRIPT}` and `${CONDA_RUN} bash ${SCRIPT}`. Both come from the calling workflow and need double quotes.

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

I fixed all four findings, all in action.yml. Nothing has been run or tested yet.

- **Unpinned action:** `actions/cache@v3` is now pinned to the commit SHA that v3 currently points to, `6f8efc29b200d32929f49075959781ed54ec270c`, with a `# v3` comment so it stays readable.
- **Inline expression:** `inputs.is_windows` is now passed in through `env:` as `IS_WINDOWS` and checked as `"${IS_WINDOWS}"`, so it is no longer pasted straight into the script.
- **Unquoted variables:** every use of `SCRIPT` is now in double quotes.
- **`CONDA_RUN`:** I did not simply quote this one, even though the finding asks for it. It holds a command prefix (something like `conda run -p <env>`), and quoting it would pass the whole thing as one word, so the script would try to run a program with that full name and fail. Instead it is split into an array the same way upstream split it, by assigning it unquoted, and run as `${conda_run[@]+"${conda_run[@]}"}`. That form is safe under `set -u` (strict mode errors on unset variables) and drops out entirely when `CONDA_RUN` is empty. An unquoted expansion only splits on spaces and expands wildcards; it doesn't run anything inside the value, so this is not an injection risk. A scanner that wants every variable quoted may still flag this line.

