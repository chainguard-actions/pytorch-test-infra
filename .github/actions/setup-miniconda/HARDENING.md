<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261103-202628** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml composite steps use actions by mutable tag rather than a full 40-char commit SHA: line 47 'uses: actions/cache@v3' and line 105 'uses: actions/cache@v3'.

Locations:

- `action.yml:47`
- `action.yml:105`

### script-injection (severity: high)

Rule (a): step 'Get date' interpolates an expression directly into the run script: 'echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"'. A crafted input such as '$(cmd)' or '; cmd' would be executed. Move it into an env: variable and quote it.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a): step 'Setup conda environment with python' interpolates '${{ inputs.default-packages }}' directly into the conda create command (line 139). Rule (b): the unquoted '${ENV_FILE_FLAG}' (line 137) expands workflow-controlled data from inputs.environment-file (set via ENV_FILE_FLAG="--file ${ENV_FILE}" at line 123). Move the input into env: and use a properly quoted or array form.

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

Step 'Update GitHub path to include miniconda install' writes 'echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"' to $GITHUB_ENV. PATH is inherited from the calling workflow and is not computed in this script, and it is written without the printf '%s' ... | tr -d '\n\r' sanitization step. That could allow newline injection of extra environment variables.

Locations:

- `action.yml:90`

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

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned both actions/cache@v3 uses to 6f8efc29b200d32929f49075959781ed54ec270c. Moved inputs.default-packages into env (DEFAULT_PACKAGES) in both 'Get date' and 'Setup conda environment' steps, and split it into an array with the quote-aware xargs method, which matches how upstream's inline expression was split. The checksum is still taken over the space-joined package list, so cache keys come out the same for normal inputs. ENV_FILE_FLAG is now a bash array (--file "$ENV_FILE"). The PATH value written to GITHUB_ENV now has newlines stripped with printf | tr -d '\n\r'.

