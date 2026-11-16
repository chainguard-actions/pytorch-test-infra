<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261109-232755** was hardened automatically. 7 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The input value is pasted into the shell script before it runs, so a crafted value can run commands. Fix: pass the input through an env: variable and use it double-quoted.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a): the 'Setup conda environment with python' step puts `${{ inputs.default-packages }}` straight into the `conda create` command in its run script. Rule (b): the same step expands `${ENV_FILE_FLAG}` unquoted. That variable is built from the workflow-controlled `ENV_FILE` input (`ENV_FILE_FLAG="--file ${ENV_FILE}"`), and the line is not an array assignment covered by a shellcheck directive.

Locations:

- `action.yml:139`
- `action.yml:137`

### unpinned-uses (severity: high)

Two composite steps use a tag instead of a full commit SHA: `uses: actions/cache@v3` ('Setup miniconda cache') and `uses: actions/cache@v3` ('Setup miniconda env cache').

Locations:

- `action.yml:47`
- `action.yml:105`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes inherited process env values (`RUNNER_TEMP` via MINICONDA_INSTALL_PATH, and `PATH`) to $GITHUB_PATH (`echo "${MINICONDA_INSTALL_PATH}/bin" >> $GITHUB_PATH`) and $GITHUB_ENV (`echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"`). Neither value goes through `printf '%s' ... | tr -d '\n\r'` first.

Locations:

- `action.yml:86`
- `action.yml:90`

### github-env-injection (severity: high)

The 'Clone the base conda environment and update GitHub env' step writes CONDA_PREFIX to $GITHUB_ENV. CONDA_PREFIX is built from the inherited env vars `RUNNER_TEMP` and `GITHUB_RUN_ID`, and the step writes it, along with CONDA_RUNTIME, in `echo "CONDA_ENV=${CONDA_PREFIX}"`, `CONDA_PREFIX=...`, `CONDA_RUN=...` and `CONDA_INSTALL=...`. None of these values go through `printf '%s' ... | tr -d '\n\r'` first.

Locations:

- `action.yml:186`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.default-packages }}" appears directly in run: block of step "Get date"; move to env: map

Locations:

- `action.yml:43`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.default-packages }}" appears directly in run: block of step "Setup conda environment with python (v${{ inputs.python-version }})"; move to env: map

Locations:

- `action.yml:139`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses, github-env-injection

**Notes:**

I edited action.yml. The run scripts no longer contain `${{ inputs.default-packages }}`. Both steps that used it now get it through an env var, `DEFAULT_PACKAGES`. The value is split into a bash array the way the shell split it upstream: it honours quotes, rejects an unmatched quote and runs nothing inside the value. The checksum step still prints the packages joined by single spaces with `echo -n`, so the md5 stays the same and existing cache keys still match. I added `|| true` to that command because upstream ran it inside echo, where a failure never stopped the step. The `--file` option and its file name are now kept as separate words in a bash array instead of one unquoted string. One change in behaviour: a file name with spaces now stays one argument, where upstream's unquoted string split it. Both `actions/cache@v3` uses are pinned to 6f8efc29b200d32929f49075959781ed54ec270c, with a `# v3` comment. Newlines are now stripped from RUNNER_TEMP, PATH, CONDA_PREFIX and CONDA_RUNTIME before they are written to `$GITHUB_PATH` or `$GITHUB_ENV`, and `$GITHUB_PATH` is now quoted. I haven't run the action or re-run the analysis, so these fixes are untested.

