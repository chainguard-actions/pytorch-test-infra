<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20260922-155642** was hardened automatically. 8 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression directly into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The input is pasted into the shell script before bash runs, so `$(...)`, backticks or `;` in the value would execute.

Locations:

- `action.yml:42`

### script-injection (severity: high)

Rule (a): the 'Setup conda environment with python' step puts `${{ inputs.default-packages }}` directly into the `conda create` command (line 138). Rule (b): the same step expands `${ENV_FILE_FLAG}` unquoted (line 136). That variable is built from the workflow-controlled input `inputs.environment-file` (`ENV_FILE_FLAG="--file ${ENV_FILE}"`).

Locations:

- `action.yml:138`
- `action.yml:136`

### script-injection (severity: high)

Rule (b): the 'Install miniconda' step expands inherited env vars unquoted in a case statement: `case ${RUNNER_OS}-${RUNNER_ARCH} in`. In a composite action, env vars are inherited from the calling workflow, so these must be double-quoted.

Locations:

- `action.yml:59`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step forwards inherited process env vars into special files with no sanitization. It runs `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` into $GITHUB_ENV, and the GITHUB_PATH write is built from the inherited `${RUNNER_TEMP}`. Neither write is preceded by `printf '%s' ... | tr -d '\n\r'`.

Locations:

- `action.yml:85`
- `action.yml:89`

### github-env-injection (severity: high)

The 'Clone the base conda environment and update GitHub env' step writes CONDA_ENV, CONDA_PREFIX, CONDA_RUN and CONDA_INSTALL to $GITHUB_ENV. These values come from the inherited env vars RUNNER_TEMP and GITHUB_RUN_ID and from `which conda`, which depends on the inherited PATH. None of these writes is sanitized with `printf '%s' ... | tr -d '\n\r'`.

Locations:

- `action.yml:185`
- `action.yml:187`
- `action.yml:188`
- `action.yml:189`

### unpinned-uses (severity: high)

The composite action's steps use tag references instead of full commit SHAs: `uses: actions/cache@v3` (line 46) and `uses: actions/cache@v3` (line 104).

Locations:

- `action.yml:46`
- `action.yml:104`

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

I fixed all eight findings in action.yml. I haven't run the action or its tests after the changes.

- **Inline input in two steps:** I moved `inputs.default-packages` out of the run scripts and into `env:` in both the 'Get date' step and the 'Setup conda environment' step. Upstream pasted the input straight into the script, so the shell honoured quotes in the value. To keep that behaviour, the new code splits the value into a list with the quote-aware xargs method (it stops with an error if a quote is left unclosed, and does nothing if the value is empty). The checksum is still computed from `echo -n` of the space-joined package list, as before. That command used to sit inside echo, so a failure there never stopped the step; I added `|| true` to keep it that way. The checksum also has newlines stripped before it is written to GITHUB_OUTPUT.
- **Environment file flag:** `ENV_FILE_FLAG` was a single string expanded unquoted. It is now a list, `(--file "$ENV_FILE")`, so the file path stays one quoted argument. `CONDA_EXTRA_FLAGS` is now an empty list for the same reason.
- **Platform check:** `case "${RUNNER_OS}-${RUNNER_ARCH}"` is now quoted.
- **GITHUB_PATH / GITHUB_ENV writes:** newlines are now stripped from the miniconda install path and from PATH before they are written. In the clone step, the same goes for CONDA_PREFIX and the conda path from `which conda` before CONDA_ENV, CONDA_PREFIX, CONDA_RUN and CONDA_INSTALL are written.
- **Pinning:** both `actions/cache@v3` references are now pinned to commit 6f8efc29b200d32929f49075959781ed54ec270c, with `# v3` kept as a comment.

