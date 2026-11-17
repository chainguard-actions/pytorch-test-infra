<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261109-232755** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an input expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum ...)" >> "${GITHUB_OUTPUT}"`. If a caller passes shell metacharacters in default-packages, they run as commands. Fix: pass the input in through an env: variable and use it as "$DEFAULT_PACKAGES" (quoted).

Locations:

- `action.yml:42`

### script-injection (severity: high)

Rule (a): the 'Setup conda environment with python' step puts `${{ inputs.default-packages }}` directly into the `conda create` command. The template text is substituted into the script before bash parses it, so a crafted value can run arbitrary commands. Rule (b): the same step also expands `${ENV_FILE_FLAG}` unquoted. That variable is built as "--file ${ENV_FILE}" from the environment-file input, so whitespace and glob characters in the input get split and expanded. Fix: route default-packages through env: into a bash array (for example `read -ra` or a shellcheck-annotated array assignment). Build the env file flag as an array, e.g. `ENV_FILE_ARGS=(--file "$ENV_FILE")`, and expand it as "${ENV_FILE_ARGS[@]}".

Locations:

- `action.yml:138`
- `action.yml:136`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes the inherited process variable PATH to $GITHUB_ENV without sanitizing it: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside a `{ ... } >> "${GITHUB_ENV}"` group. PATH is not set in this script; it comes from the calling workflow. A value containing a newline could inject extra environment variables. Fix: clean it first with `printf '%s' "$PATH" | tr -d '\n\r'` before writing.

Locations:

- `action.yml:89`

### unpinned-uses (severity: high)

Composite action steps refer to actions by a mutable tag instead of a full commit SHA: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache). Pin both to a 40-character commit SHA.

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

Pinned both actions/cache@v3 uses to 6f8efc29b200d32929f49075959781ed54ec270c. Moved inputs.default-packages into env: DEFAULT_PACKAGES in both the 'Get date' step and the conda create step. Upstream pasted that input straight into the script as a ${{ }} expression, so the shell honoured quotes in it. To match that, the value is now split with the quote-aware xargs method into a bash array. The split is guarded for empty values, uses xargs -r, and checks first for an unmatched quote. The array is then expanded quoted. The checksum is still taken from the space-joined tokens, as before. ENV_FILE_FLAG is replaced with an ENV_FILE_ARGS=(--file "$ENV_FILE") array, expanded as "${ENV_FILE_ARGS[@]}". PATH now goes through tr -d '\n\r' before it is written to GITHUB_ENV.

