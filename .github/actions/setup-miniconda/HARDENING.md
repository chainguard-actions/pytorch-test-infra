<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261112-155209** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): step 'Get date' puts an expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The input is pasted into the shell text before bash runs, so a value containing $(...), backticks or ';' will execute. Fix: move it into an env var and expand it quoted, e.g. `printf '%s' "$DEFAULT_PACKAGES" | md5sum`.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Step 'Setup conda environment with python' breaks two rules. Rule (a): `${{ inputs.default-packages }} \` sits directly inside the conda create command, so a crafted value can inject shell commands. Rule (b): `${ENV_FILE_FLAG} \` is expanded unquoted. It is built from ENV_FILE (inputs.environment-file) via `ENV_FILE_FLAG="--file ${ENV_FILE}"`, so the file path gets split on whitespace and glob-expanded. Fix: pass default-packages through env (for example, read it into an array with a shellcheck-annotated `NAME=($VAR)` split) and pass the env file as quoted separate arguments: `--file "$ENV_FILE"`.

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

Step 'Update GitHub path to include miniconda install' writes `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` to $GITHUB_ENV. This forwards the inherited process env var PATH, which the calling workflow controls, and does not strip newlines first with `printf '%s' ... | tr -d '\n\r'`. A newline in the value would let the caller inject extra environment variables.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

The composite action references actions by mutable tag instead of a full commit SHA: `uses: actions/cache@v3` on line 47 (Setup miniconda cache) and `uses: actions/cache@v3` on line 105 (Setup miniconda env cache).

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

Moved inputs.default-packages into an env var (DEFAULT_PACKAGES) in both 'Get date' and 'Setup conda environment' steps. Both steps split it into an array with an unquoted assignment (shellcheck-annotated), which splits it on whitespace like upstream. The checksum hashes the array's words joined by single spaces, so it comes out the same as upstream's 'echo -n'. ENV_FILE_FLAG is now an array (--file "$ENV_FILE"), expanded quoted. Newlines are stripped from the PATH value before it is written to GITHUB_ENV. Pinned both actions/cache@v3 uses to 6f8efc29b200d32929f49075959781ed54ec270c.

