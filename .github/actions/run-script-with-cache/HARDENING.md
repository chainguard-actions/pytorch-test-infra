<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--run-script-with-cache/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--run-script-with-cache/v20261109-232755** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points to a mutable tag rather than a full 40-character commit SHA: `uses: actions/cache@v3`.

Locations:

- `action.yml:39`

### script-injection (severity: high)

The 'Run script' step breaks rule (a) and rule (b). Rule (a): an expression is substituted straight into the run script: `if [[ ${{ inputs.is_windows }} == 'disabled' ]]; then`. Fix: pass inputs.is_windows through env and compare "$IS_WINDOWS". Rule (b): environment variables holding workflow-controlled data are expanded without quotes. SCRIPT comes from inputs.script. CONDA_RUN is inherited from the calling workflow. Unquoted expansions: `if [[ ! -f ${SCRIPT} ]]; then`, `if [[ ${SCRIPT} == *.bat ]]; then`, `${CONDA_RUN} ${SCRIPT}` and `${CONDA_RUN} bash ${SCRIPT}`. Fix: write these as "$SCRIPT". Also treat the CONDA_RUN command prefix as untrusted.

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

- **unpinned-uses:** `actions/cache@v3` is now pinned to its full commit SHA, `6f8efc29b200d32929f49075959781ed54ec270c`, with `# v3` kept as a comment.
- **script-injection / static-inline-injection:** `inputs.is_windows` is now passed in through `env:` as `IS_WINDOWS` and compared as `"$IS_WINDOWS"`, so no expression is pasted into the script. Every use of `$SCRIPT` is now double-quoted.
- **CONDA_RUN:** this variable holds a command plus its arguments (for example `conda run -p <env>`), so it still has to be split into separate words. I split it into an array in the same unquoted way upstream did, which runs nothing inside the value. I then expand it as `${conda_run[@]+"${conda_run[@]}"}`. That form still works when `CONDA_RUN` is empty under `set -u`, including on older bash (3.2).

Nothing was run or tested after these edits.

