<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261109-192709** was hardened automatically. 8 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an input expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The value of inputs.default-packages is substituted into the script text before the shell parses it, so a crafted value can run commands. Fix: set DEFAULT_PACKAGES from the input in env: and use "$DEFAULT_PACKAGES" in double quotes.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a): the 'Setup conda environment with python' step puts an input expression straight into the run script: `${{ inputs.default-packages }} \` inside the `conda create` command. Rule (b) also fails in this step: ENV_FILE_FLAG="--file ${ENV_FILE}" comes from inputs.environment-file and is expanded unquoted as `${ENV_FILE_FLAG} \`. This line is not an array assignment and has no shellcheck directive, so the exemption does not apply. Fix: set the input in env: and expand it into a bash array, or quote the expansion.

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

The 'Get date' step writes a value built from inputs.default-packages to $GITHUB_OUTPUT (`echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum ...)" >> "${GITHUB_OUTPUT}"`). The input expression is substituted directly, and the `printf '%s' ... | tr -d '\n\r'` step does not run before the write.

Locations:

- `action.yml:43`

### github-env-injection (severity: high)

The 'Update GitHub path' step copies inherited process env vars that this script does not set (RUNNER_TEMP via MINICONDA_INSTALL_PATH, and PATH) into the special files without sanitizing them: `echo "${MINICONDA_INSTALL_PATH}/bin" >> $GITHUB_PATH` and `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` ... `>> "${GITHUB_ENV}"`. Neither write is preceded by `printf '%s' ... | tr -d '\n\r'`. The calling workflow controls these env vars in a composite action. The $GITHUB_PATH redirect target is also unquoted.

Locations:

- `action.yml:86`
- `action.yml:90`

### github-env-injection (severity: high)

The 'Clone the base conda environment' step writes CONDA_PREFIX and CONDA_RUNTIME to $GITHUB_ENV without sanitizing them. CONDA_PREFIX is built from the inherited RUNNER_TEMP, and CONDA_RUNTIME comes from `which conda`, which depends on PATH. The affected lines are `echo "CONDA_ENV=${CONDA_PREFIX}"`, `echo "CONDA_PREFIX=..."`, `echo "CONDA_RUN=${CONDA_RUNTIME} run -p ${CONDA_PREFIX} ..."` and `echo "CONDA_INSTALL=..."`, all followed by `>> "${GITHUB_ENV}"`. None of them uses `printf '%s' ... | tr -d '\n\r'` first.

Locations:

- `action.yml:186`

### unpinned-uses (severity: high)

Two composite steps reference an action by a mutable tag instead of a full commit SHA: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

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

**Fixes applied:** script-injection, github-env-injection, unpinned-uses, static-inline-injection

**Notes:**

All changes are in action.yml. Nothing was run or tested.

- **Input in scripts:** `inputs.default-packages` now reaches the 'Get date' and 'Setup conda environment' steps through an env var, `DEFAULT_PACKAGES`. Upstream pasted the input straight into the script, so the shell honoured quotes in the value. To keep that behaviour, the value is split into an array with the quote-aware xargs method, including the empty-value guard and the `xargs -r true` check for unmatched quotes. One difference: package specs containing `*` (for example `numpy=1.*`) are no longer expanded against filenames.
- **Cache key:** the checksum is taken over the split packages joined by single spaces, which matches what upstream's `echo -n` produced. Newlines are removed before it is written to `GITHUB_OUTPUT`.
- **Env file flag:** `ENV_FILE_FLAG` is now an array, `(--file "$ENV_FILE")`, and `CONDA_EXTRA_FLAGS` is an empty array. Both are expanded as quoted arrays.
- **Writes to GITHUB_PATH / GITHUB_ENV:** `RUNNER_TEMP`, `PATH`, `CONDA_PREFIX` and `CONDA_RUNTIME` have newlines stripped before they are written. The redirect to `$GITHUB_PATH` is now quoted.
- **Pinned action:** both `actions/cache@v3` references are pinned to commit 6f8efc29b200d32929f49075959781ed54ec270c, with `# v3` kept as a comment.

