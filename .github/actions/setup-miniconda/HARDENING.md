<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261021-234439** was hardened automatically. 7 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): in the 'Get date' step, the inputs.default-packages expression is placed directly in the run: script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. Whoever calls the action can put shell metacharacters (`$(...)`, `;`, backticks) in this input and they will run.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a): in the 'Setup conda environment with python' step, `${{ inputs.default-packages }} \` is placed directly in the conda create command line. Rule (b): `${ENV_FILE_FLAG} \` expands unquoted, and its value comes from inputs.environment-file (`ENV_FILE_FLAG="--file ${ENV_FILE}"`). That lets the shell split the value on whitespace and expand glob characters from the input.

Locations:

- `action.yml:139`
- `action.yml:137`

### script-injection (severity: high)

Rule (b): in the 'Install miniconda' step, the case statement uses unquoted expansions: `case ${RUNNER_OS}-${RUNNER_ARCH} in`. The check requires env-var expansions to be double-quoted, including in case words. Use `case "${RUNNER_OS}-${RUNNER_ARCH}" in`.

Locations:

- `action.yml:60`

### github-env-injection (severity: high)

In the 'Update GitHub path to include miniconda install' step, the inherited process env var PATH is written into $GITHUB_ENV without the required sanitization: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside a `{ ... } >> "${GITHUB_ENV}"` group. The calling workflow controls PATH, and the value is not passed through `printf '%s' ... | tr -d '\n\r'` first, so a newline in it could add extra environment variables.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

Composite steps reference actions by a mutable tag instead of a full commit SHA: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

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

action.yml: moved inputs.default-packages into env (DEFAULT_PACKAGES) in both steps, tokenized with the quote-aware xargs split (matching upstream's inline expression semantics); checksum computed from the space-joined tokens (same as echo -n). ENV_FILE_FLAG converted to a bash array (--file "$ENV_FILE"); dropped empty CONDA_EXTRA_FLAGS. Quoted case word "${RUNNER_OS}-${RUNNER_ARCH}". PATH sanitized with tr -d '\n\r' before writing to GITHUB_ENV; quoted $GITHUB_PATH. Pinned actions/cache@v3 to 6f8efc29b200d32929f49075959781ed54ec270c in both places.

