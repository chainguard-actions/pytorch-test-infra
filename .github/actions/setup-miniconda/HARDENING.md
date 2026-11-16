<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261103-202628** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): an expression is placed straight into a run: script in the 'Get date' step: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum ...)" >> "${GITHUB_OUTPUT}"`. The input is substituted into the script text before the shell runs, so a crafted value can run commands. Fix: pass it in through an env: variable and quote it ("$DEFAULT_PACKAGES").

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a): `${{ inputs.default-packages }}` is placed straight into the conda create command in the 'Setup conda environment with python' step (line 139). Rule (b): in the same step, `${ENV_FILE_FLAG}` is expanded unquoted (line 137). Its value contains the environment-file input (`ENV_FILE_FLAG="--file ${ENV_FILE}"`), and this is not a shellcheck-annotated array assignment. Fix: pass default-packages in through env: and expand it in a controlled way, such as a shellcheck-annotated array. Pass the env file as separate quoted arguments (--file "$ENV_FILE").

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

In the 'Update GitHub path to include miniconda install' step, the composite action writes the inherited PATH variable to $GITHUB_ENV without sanitizing it first: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside `{ ... } >> "${GITHUB_ENV}"`. The calling workflow controls PATH, and the value does not go through printf '%s' ... | tr -d '\n\r' before the write, so an embedded newline could inject extra environment variables.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

Composite steps in action.yml use tag refs instead of full commit SHAs: `uses: actions/cache@v3` (line 47, Setup miniconda cache) and `uses: actions/cache@v3` (line 105, Setup miniconda env cache).

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

Pinned both actions/cache@v3 to 6f8efc29b200d32929f49075959781ed54ec270c (# v3). Moved inputs.default-packages into env (DEFAULT_PACKAGES) in both steps. Since upstream pasted the expression straight into the script, the value is now split into a bash array with the quote-aware xargs method (guarded for empty values, fails on an unmatched quote). The checksum hashes the space-joined array, the same text upstream's `echo -n` produced, so cache keys stay the same. ENV_FILE_FLAG is now an array (--file "$ENV_FILE") expanded as "${ENV_FILE_FLAG[@]}". The PATH written to GITHUB_ENV now has newlines and carriage returns removed with printf/tr before it is written.

