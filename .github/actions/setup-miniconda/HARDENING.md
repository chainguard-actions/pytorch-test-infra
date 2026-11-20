<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261119-192116** was hardened automatically. 7 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): in the 'Get date' step, the expression is placed straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum ...)"`. The input is pasted into the shell script before bash runs it, so shell metacharacters in it can run commands. Move it into an env: variable and expand it double-quoted.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (b): in the 'Install miniconda' step, `case ${RUNNER_OS}-${ARCH} in` expands ARCH (taken from steps.arch.outputs.arch) without quotes. It should be `case "${RUNNER_OS}-${ARCH}" in`.

Locations:

- `action.yml:74`

### script-injection (severity: high)

Rule (a): in the 'Setup conda environment with python' step, `${{ inputs.default-packages }}` is placed straight into the run script as conda create arguments. Rule (b): the same step expands `${ENV_FILE_FLAG}` without quotes. That variable holds `--file ${ENV_FILE}`, where ENV_FILE comes from inputs.environment-file, so the input reaches the shell unquoted. This is not an array assignment with a shellcheck directive, so the exemption does not apply.

Locations:

- `action.yml:153`
- `action.yml:151`

### github-env-injection (severity: high)

In the 'Update GitHub path to include miniconda install' step, `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` is written to $GITHUB_ENV. PATH is inherited from the calling workflow, not computed in this script, and no `printf '%s' ... | tr -d '\n\r'` step cleans it first, so a newline in it could add extra environment variables.

Locations:

- `action.yml:104`

### unpinned-uses (severity: high)

Composite steps in action.yml reference actions by a mutable tag instead of a full commit SHA: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

Locations:

- `action.yml:60`
- `action.yml:119`

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

Moved inputs.default-packages into env (DEFAULT_PACKAGES) in both 'Get date' and 'Setup conda environment' steps; tokenized with the quote-aware xargs split (matches upstream's inline ${{ }} splitting) into an array used for the checksum (echo -n joins with single spaces as before) and as conda create args. ENV_FILE_FLAG is now a bash array (--file "$ENV_FILE"). Quoted case "${RUNNER_OS}-${ARCH}". PATH written to GITHUB_ENV is sanitized via printf|tr -d '\n\r'; quoted $GITHUB_PATH. Pinned actions/cache@v3 to 6f8efc29b200d32929f49075959781ed54ec270c.

