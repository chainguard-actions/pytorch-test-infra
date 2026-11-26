<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261125-223308** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses a mutable tag instead of a full 40-character commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Step 'Run script' breaks rule (a): an expression is placed straight into the run script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. Pass it through env (e.g. IS_WINDOWS) and quote it as "$IS_WINDOWS".

Locations:

- `action.yml:51`

### script-injection (severity: high)

Step 'Run script' breaks rule (b): variables holding values the calling workflow controls are expanded without quotes. SCRIPT comes from inputs.script and CONDA_RUN is inherited from the calling workflow: `if [[ ! -f ${SCRIPT} ]]; then`, `if [[ ${SCRIPT} == *.bat ]]; then`, `${CONDA_RUN} ${SCRIPT}`, `${CONDA_RUN} bash ${SCRIPT}`. Quote them as "${SCRIPT}".

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

Pinned actions/cache@v3 to 6f8efc29b200d32929f49075959781ed54ec270c. Moved inputs.is_windows into env as IS_WINDOWS and quoted it. SCRIPT is now quoted everywhere it is used. CONDA_RUN is a command prefix such as 'conda run -p ...', so quoting it as one word would break it. Instead it is split into a bash array with the same whitespace split upstream got from leaving it unquoted, and that array is expanded quoted. The guarded expansion keeps it safe under set -u when CONDA_RUN is empty. Nothing was run to test these changes.

