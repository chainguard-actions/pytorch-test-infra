<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261123-205410

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261123-205410** was hardened automatically. 8 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression straight into the run: script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. Because inputs.default-packages is pasted into the script before the shell runs, a crafted value can run commands. Fix: pass it through env: and expand it quoted.

Locations:

- `action.yml:42`

### script-injection (severity: high)

Rule (a): the 'Setup conda environment with python' step puts `${{ inputs.default-packages }} \` straight into the conda create command in its run: script. Rule (b) also applies: `${ENV_FILE_FLAG} \` (built from inputs.environment-file) is expanded unquoted. It is not an array assignment and has no shellcheck directive, so the exemption does not apply.

Locations:

- `action.yml:152`
- `action.yml:150`

### script-injection (severity: high)

Rule (b): the 'Install miniconda' step expands workflow-controlled data unquoted in a case statement: `case ${RUNNER_OS}-${ARCH} in`. ARCH comes from steps.arch.outputs.arch. It should be written as `case "${RUNNER_OS}-${ARCH}" in`.

Locations:

- `action.yml:73`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes values built from inherited process env vars (RUNNER_TEMP, PATH) to $GITHUB_PATH and $GITHUB_ENV without first running printf '%s' ... | tr -d '\n\r'. The writes are `echo "${MINICONDA_INSTALL_PATH}/bin" >> $GITHUB_PATH` and `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` redirected to "${GITHUB_ENV}".

Locations:

- `action.yml:99`
- `action.yml:103`

### github-env-injection (severity: high)

The 'Clone the base conda environment and update GitHub env' step writes CONDA_ENV, CONDA_PREFIX, CONDA_RUN and CONDA_INSTALL to $GITHUB_ENV without sanitizing them. These values come from inherited env vars (RUNNER_TEMP, GITHUB_RUN_ID) and from the output of `which conda`, e.g. `echo "CONDA_ENV=${CONDA_PREFIX}" >> "${GITHUB_ENV}"`. No printf '%s' | tr -d '\n\r' step comes before the writes.

Locations:

- `action.yml:199`

### unpinned-uses (severity: high)

Two composite steps reference an action by a mutable tag instead of a full commit SHA: `uses: actions/cache@v3` ('Setup miniconda cache') and `uses: actions/cache@v3` ('Setup miniconda env cache').

Locations:

- `action.yml:59`
- `action.yml:118`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.default-packages }}" appears directly in run: block of step "Get date"; move to env: map

Locations:

- `action.yml:43`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.default-packages }}" appears directly in run: block of step "Setup conda environment with python (v${{ inputs.python-version }})"; move to env: map

Locations:

- `action.yml:153`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, github-env-injection, unpinned-uses, static-inline-injection

**Notes:**

I fixed every finding in action.yml. Nothing was run or tested after the changes.

- **Pinned actions:** both actions/cache@v3 references now point to the full commit SHA 6f8efc29b200d32929f49075959781ed54ec270c, with a `# v3` comment so the version is still readable.
- **default-packages input:** it no longer goes straight into the scripts. Both the 'Get date' step and the conda create step now read it from an env var, DEFAULT_PACKAGES. Upstream pasted the value into the script, so the shell respected quotes inside it. To keep that, each step splits it into an array using the xargs method that respects quotes, guarded against empty values and unmatched quotes. The checksum is still taken from `echo -n` of the words joined by spaces, which gives the same result as upstream, so existing cache keys should stay the same.
- **Environment file flag:** ENV_FILE_FLAG is now an array, `(--file "$ENV_FILE")`, so the file path is passed as one quoted value. The empty CONDA_EXTRA_FLAGS is also an array now, and both are expanded quoted.
- **case statement:** it now reads `case "${RUNNER_OS}-${ARCH}" in`.
- **Writes to GITHUB_PATH and GITHUB_ENV:** the miniconda install path, PATH, CONDA_PREFIX and the `which conda` result now have newlines stripped (`printf '%s' | tr -d '\n\r'`) before they are written. `$GITHUB_PATH` is also quoted now.

