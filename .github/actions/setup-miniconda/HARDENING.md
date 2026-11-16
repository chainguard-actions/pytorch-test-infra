<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261029-163400** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression straight into the run: script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. Whoever calls the action can set inputs.default-packages to inject shell commands. Fix: pass it through an env: variable and quote that variable.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a): the 'Setup conda environment with python' step puts `${{ inputs.default-packages }}` straight into the conda create command in run: (line 139). The step also breaks rule (b): `${ENV_FILE_FLAG}` (line 137) is expanded unquoted, and it holds the workflow-controlled input inputs.environment-file (ENV_FILE_FLAG="--file ${ENV_FILE}"). Fix: pass default-packages through env: and expand it into a properly hardened array. Build the --file flag as a quoted array, e.g. `--file "$ENV_FILE"`.

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes the inherited process env var PATH to $GITHUB_ENV with no sanitization: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside `{ ... } >> "${GITHUB_ENV}"`. In a composite action the calling workflow controls PATH. Fix: sanitize it with `printf '%s' "$PATH" | tr -d '\n\r'` before the write.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

The composite action steps in action.yml use tag refs instead of full commit SHAs: `uses: actions/cache@v3` (line 47) and `uses: actions/cache@v3` (line 105).

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

I fixed all four findings in action.yml. Nothing has been run or tested yet.

- **Script injection (`inputs.default-packages`):** in both the 'Get date' step and the 'Setup conda environment' step, the input now goes through the step's env: block as DEFAULT_PACKAGES. Each step then splits it into a bash array with the quote-aware xargs method, which reads quotes the same way upstream's inline expression did. An empty input gives no arguments, and an input with an unmatched quote stops the step.
- **Checksum:** the checksum is now computed from that array with `echo -n`, so the hash matches what upstream produced. A failure still doesn't stop the step, same as upstream.
- **Unquoted `--file` flag:** ENV_FILE_FLAG and CONDA_EXTRA_FLAGS are now bash arrays, with the file path quoted (`--file "$ENV_FILE"`).
- **PATH written to $GITHUB_ENV:** newlines and carriage returns are stripped from PATH with `printf '%s' "$PATH" | tr -d '\n\r'` before it is written. I also quoted `$GITHUB_PATH` in the same step.
- **Unpinned actions:** both `actions/cache@v3` references are pinned to 6f8efc29b200d32929f49075959781ed54ec270c, with a `# v3` comment.

