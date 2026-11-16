<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20260922-155642** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The inputs.default-packages value is inserted into the script before bash parses it, so a caller can run shell commands through it. Fix: pass it in through an env: variable and expand that variable with double quotes.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Two problems in the step 'Setup conda environment with python'. Rule (a): `${{ inputs.default-packages }} \` is inserted straight into the `conda create` command line. Rule (b): `${ENV_FILE_FLAG} \` is expanded without quotes, and it holds the workflow-controlled value inputs.environment-file (ENV_FILE_FLAG="--file ${ENV_FILE}"). This is a plain variable, not an array assignment with a shellcheck directive, so the exemption does not apply. Fix: pass default-packages through env: and expand it in a safe way, and build the --file option from a quoted "$ENV_FILE", for example with a bash array.

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

The step 'Update GitHub path to include miniconda install' writes the inherited process variable $PATH to $GITHUB_ENV (`echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside a block appended to "${GITHUB_ENV}") without first stripping newlines with `printf '%s' ... | tr -d '\n\r'`. PATH is inherited from the calling workflow's environment, so a value containing a newline could add extra environment variables.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

Composite steps use a version tag instead of a full commit SHA: `uses: actions/cache@v3` (line 47, 'Setup miniconda cache') and `uses: actions/cache@v3` (line 105, 'Setup miniconda env cache'). Pin both to a 40-character commit SHA.

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

I moved inputs.default-packages into env: DEFAULT_PACKAGES in the 'Get date' step and the 'Setup conda environment' step. Upstream pasted the value straight into the script, so the shell split it into words and honoured quotes. To keep that behaviour, each step now splits it into an array with the quote-aware xargs method: an empty value is skipped and an unmatched quote stops the step. The array is then passed as "${pkgs[@]}". The checksum comes out the same as before, because echo -n of the array joins the words with single spaces. ENV_FILE_FLAG is now an array, (--file "$ENV_FILE"), passed as "${ENV_FILE_FLAG[@]}". Before the PATH line is written to GITHUB_ENV, newlines are now stripped with printf | tr -d '\n\r'. Both actions/cache@v3 uses are pinned to 6f8efc29b200d32929f49075959781ed54ec270c (# v3), which is the commit the v3 tag points to. I haven't run the changed workflow.

