<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261103-202628** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references an action by a mutable tag rather than a 40-char commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

Step 'Run script': (a) a GitHub expression is interpolated directly into the run script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. Pass it through an env var and double-quote it instead. (b) The workflow-controlled env vars are expanded without quotes: `if [[ ! -f ${SCRIPT} ]]; then`, `if [[ ${SCRIPT} == *.bat ]]; then`, `${CONDA_RUN} ${SCRIPT}` and `${CONDA_RUN} bash ${SCRIPT}`. SCRIPT comes from inputs.script. CONDA_RUN is inherited from the calling workflow.

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

I pinned actions/cache@v3 to its commit SHA 6f8efc29b200d32929f49075959781ed54ec270c and kept '# v3' as a comment. In the 'Run script' step, inputs.is_windows now comes in through an IS_WINDOWS env var and is double-quoted, and every use of SCRIPT is double-quoted. CONDA_RUN is a command prefix made of several words, so I split it into an array with an unquoted assignment. That splits it into words the same way upstream's unquoted expansion did. The array is expanded with ${arr[@]+...} so an unset or empty CONDA_RUN doesn't trip set -u on older bash. Nothing was run or tested. The changes only touch action.yml.

