<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261109-192709** was hardened automatically. 8 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The input is substituted into the script text before bash parses it, so a caller can run any command. Fix: pass inputs.default-packages through an env: variable and use it double-quoted.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a): the 'Setup conda environment with python' step puts `${{ inputs.default-packages }} \` straight into the run script as conda create arguments. Rule (b) also applies: `ENV_FILE_FLAG="--file ${ENV_FILE}"` copies inputs.environment-file into a variable, which is then expanded unquoted as `${ENV_FILE_FLAG} \`. That is not a guarded array assignment, so the exemption does not apply. Fix: route default-packages through env: and build arguments with quoted arrays, e.g. args=(--file "$ENV_FILE") and "${args[@]}".

Locations:

- `action.yml:139`
- `action.yml:137`
- `action.yml:123`

### script-injection (severity: high)

Rule (b): the 'Install miniconda' step expands inherited env vars without quotes in a case statement: `case ${RUNNER_OS}-${RUNNER_ARCH} in`. The check says a case subject must be double-quoted: `case "${RUNNER_OS}-${RUNNER_ARCH}" in`. The risk is low, because the runner sets these variables and bash does not word-split a case subject.

Locations:

- `action.yml:60`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes values built from inherited process env vars (RUNNER_TEMP, PATH) to $GITHUB_PATH and $GITHUB_ENV without sanitizing them first: `echo "${MINICONDA_INSTALL_PATH}/bin" >> $GITHUB_PATH` and `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` / `echo "CONDA_EXE=..."` >> "${GITHUB_ENV}". The check requires `printf '%s' ... | tr -d '\n\r'` before each write.

Locations:

- `action.yml:86`
- `action.yml:90`

### github-env-injection (severity: high)

The 'Clone the base conda environment and update GitHub env' step writes CONDA_ENV, CONDA_PREFIX, CONDA_RUN and CONDA_INSTALL to $GITHUB_ENV without sanitizing them first. These values come from inherited env (RUNNER_TEMP, GITHUB_RUN_ID) and from `which conda`, which depends on the inherited PATH. For example: `echo "CONDA_RUN=${CONDA_RUNTIME} run -p ${CONDA_PREFIX} --no-capture-output" >> "${GITHUB_ENV}"`. The check requires `printf '%s' ... | tr -d '\n\r'` before each write.

Locations:

- `action.yml:186`
- `action.yml:188`
- `action.yml:189`
- `action.yml:190`

### unpinned-uses (severity: high)

The composite steps use mutable tag refs instead of full commit SHAs: `uses: actions/cache@v3` (line 47) and `uses: actions/cache@v3` (line 105). Pin both to a 40-character commit SHA.

Locations:

- `action.yml:47`
- `action.yml:105`

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

**Fixes applied:** script-injection, static-inline-injection, github-env-injection, unpinned-uses

**Notes:**

Moved inputs.default-packages into env: (DEFAULT_PACKAGES) in both 'Get date' and 'Setup conda environment' steps; it is now tokenized with the quote-aware xargs split (with the unmatched-quote check and empty guard) and expanded as "${PKG_ARGS[@]}". The checksum is computed from the tokens joined by single spaces ("${pkgs[*]}"), which matches upstream's echo -n output, so cache keys are unchanged. Replaced the ENV_FILE_FLAG string with an array: (--file "$ENV_FILE"). Removed the unused, always-empty CONDA_EXTRA_FLAGS. Quoted the case subject. Every value written to GITHUB_PATH/GITHUB_ENV now goes through printf '%s' | tr -d '\n\r' first. Pinned both actions/cache@v3 references to 6f8efc29b200d32929f49075959781ed54ec270c.

