<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261112-155209** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml uses a mutable tag rather than a full commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Step 'Run script': (a) A GitHub expression is placed directly inside the run script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. (b) Variables holding workflow-controlled data are expanded without quotes: `if [[ ! -f ${SCRIPT} ]]; then`, `if [[ ${SCRIPT} == *.bat ]]; then`, `${CONDA_RUN} ${SCRIPT}`, `${CONDA_RUN} bash ${SCRIPT}`. SCRIPT comes from inputs.script. CONDA_RUN is inherited from the calling workflow's environment.

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

I pinned actions/cache@v3 to its full commit SHA 6f8efc29b200d32929f49075959781ed54ec270c, which I looked up rather than guessed. In the 'Run script' step, the inputs.is_windows expression now goes in through the step's env: block as IS_WINDOWS and is compared with quotes. Every use of SCRIPT is now double-quoted. CONDA_RUN is a command prefix (like "conda run -p ..."), so it still has to split into separate words. It is loaded into a bash array with an unquoted assignment, which splits it the same way upstream's unquoted expansion did. The array is then expanded in a form that is still safe under 'set -u' when CONDA_RUN is empty (older bash, such as macOS's 3.2, fails on an empty array otherwise). Nothing was run to test these changes.

