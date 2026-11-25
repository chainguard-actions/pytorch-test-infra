<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261125-022556

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261125-022556** was hardened automatically. 8 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum ...)" >> "${GITHUB_OUTPUT}"`. The input value is pasted into the script text before the shell parses it, so shell metacharacters in the input run as commands.

Locations:

- `action.yml:43`

### script-injection (severity: high)

The 'Setup conda environment with python' step breaks two rules. Rule (a): `${{ inputs.default-packages }} \` is placed straight into the conda create command. Rule (b): `${ENV_FILE_FLAG} \` is expanded without quotes. Its value comes from the environment-file input (ENV_FILE_FLAG="--file ${ENV_FILE}"), and this is a command argument, not an array assignment with a shellcheck directive, so the exception does not apply.

Locations:

- `action.yml:153`
- `action.yml:151`

### script-injection (severity: high)

Rule (b): the 'Install miniconda' step runs `case ${RUNNER_OS}-${ARCH} in` without quotes. ARCH comes from the env value `${{ steps.arch.outputs.arch }}`, which is workflow data, so it should be quoted: `case "${RUNNER_OS}-${ARCH}" in`.

Locations:

- `action.yml:74`

### unpinned-uses (severity: high)

Two composite steps pin actions/cache to a version tag instead of a full commit SHA: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

Locations:

- `action.yml:60`
- `action.yml:119`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` to $GITHUB_ENV. PATH and RUNNER_TEMP are inherited process env vars that the calling workflow controls, and the value goes through no `printf '%s' ... | tr -d '\n\r'` step first. The `$GITHUB_PATH` write built from RUNNER_TEMP has no sanitization either.

Locations:

- `action.yml:100`
- `action.yml:104`

### github-env-injection (severity: high)

The 'Clone the base conda environment and update GitHub env' step writes CONDA_ENV, CONDA_PREFIX, CONDA_RUN and CONDA_INSTALL to $GITHUB_ENV with no `printf '%s' ... | tr -d '\n\r'` step. These values are built from inherited env vars (RUNNER_TEMP, GITHUB_RUN_ID) and from the output of `which conda`, which depends on the inherited PATH. For example: `echo "CONDA_PREFIX=${CONDA_PREFIX}" >> "${GITHUB_ENV}"`.

Locations:

- `action.yml:200`

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

**Fixes applied:** script-injection, unpinned-uses, github-env-injection, static-inline-injection

**Notes:**

I fixed all eight findings in action.yml.

- **Script injection (`default-packages`):** the input no longer goes straight into the shell script, in both the 'Get date' step and the 'Setup conda environment' step. It now arrives as an environment variable, `DEFAULT_PACKAGES`. Upstream let the shell split it, so I split it into an array the same way, respecting quotes, and stop on an unmatched quote. The array is used both for the md5 checksum and for the `conda create` arguments.
- **Script injection (`ENV_FILE_FLAG`):** this is now an array, `(--file "$ENV_FILE")`, expanded as `"${ENV_FILE_FLAG[@]}"`. A file path containing spaces now stays one argument.
- **Script injection (`case` statement):** I added quotes, so it reads `case "${RUNNER_OS}-${ARCH}"`.
- **Unpinned actions:** both uses of `actions/cache@v3` are now pinned to the commit SHA `6f8efc29b200d32929f49075959781ed54ec270c`, with `# v3` kept as a comment.
- **Writes to GitHub env/path files:** the miniconda path, `PATH`, `CONDA_PREFIX` and the conda runtime path now have newlines stripped (`printf '%s' | tr -d '\n\r'`) before being written to `$GITHUB_PATH` or `$GITHUB_ENV`. I also quoted `$GITHUB_PATH`.

I didn't run the action or any tests, so these changes haven't been exercised yet. One small behaviour change: the package list is no longer glob-expanded the way the old inline version could be. That makes no difference for normal package specs like `cmake=3.22`.

