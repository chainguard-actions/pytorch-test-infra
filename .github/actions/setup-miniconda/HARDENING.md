<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261029-163400** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an input expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. A caller-supplied value that contains `$(...)`, backticks or `;` runs as shell code. Fix: pass inputs.default-packages through an env: variable and use it double-quoted.

Locations:

- `action.yml:43`

### script-injection (severity: high)

The 'Setup conda environment with python' step breaks two rules. Rule (a): `${{ inputs.default-packages }} \` is put straight into the `conda create` command, so caller-controlled text is run by the shell. Rule (b): ENV_FILE_FLAG is built from the input as `ENV_FILE_FLAG="--file ${ENV_FILE}"` (which comes from inputs.environment-file) and then used unquoted as `${ENV_FILE_FLAG} \`. This is a plain command argument, not an array assignment with a shellcheck directive, so the exemption does not apply.

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step copies the inherited `PATH` variable into GITHUB_ENV without cleaning it: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside `{ ... } >> "${GITHUB_ENV}"`. In a composite action the calling workflow controls PATH, so a value containing a newline can add extra environment variables. Fix: strip newlines first with `printf '%s' "$PATH" | tr -d '\n\r'` and write the cleaned value.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

Composite steps in action.yml use tag refs instead of full commit SHAs: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

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

action.yml: inputs.default-packages now reaches both run steps through a DEFAULT_PACKAGES env var. Upstream pasted the expression straight into the script, so the shell honoured quotes in it. To keep that behaviour, the value is split into a bash array with the quote-aware xargs method, including the check that fails on an unmatched quote. In the 'Get date' step the checksum is taken over the array joined with single spaces, which gives the same text as upstream's unquoted echo -n. ENV_FILE_FLAG is now a bash array (--file "$ENV_FILE"), so the file path stays one quoted argument. I removed CONDA_EXTRA_FLAGS, which was always empty and so passed nothing. PATH has newlines removed before it is written to GITHUB_ENV, and GITHUB_PATH is now quoted. Both actions/cache@v3 uses are pinned to 6f8efc29b200d32929f49075959781ed54ec270c # v3. I haven't run the action to test these changes.

