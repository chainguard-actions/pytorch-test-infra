<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261021-234439** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): in the 'Get date' step, an expression is placed straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The input is substituted into the script text before the shell runs, so shell metacharacters in it get executed. Fix: pass it through an env var and quote it ("$DEFAULT_PACKAGES").

Locations:

- `action.yml:40`

### script-injection (severity: high)

Rule (a): in the 'Setup conda environment with python' step, `${{ inputs.default-packages }}` is placed straight into the conda create command (line 136). Rule (b): `${ENV_FILE_FLAG}` (line 134) is expanded unquoted, and it holds the workflow-controlled ENV_FILE input (`ENV_FILE_FLAG="--file ${ENV_FILE}"`). Fix: route default-packages through an env var and expand both values in a safe form (for example a bash array built from quoted values).

Locations:

- `action.yml:136`
- `action.yml:134`

### github-env-injection (severity: high)

In the 'Update GitHub path to include miniconda install' step, the inherited process env var PATH is written to $GITHUB_ENV without sanitising it first: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside a block that redirects to "${GITHUB_ENV}". PATH is not set by this script, so the calling workflow controls it. No `printf '%s' ... | tr -d '\n\r'` is applied before the write.

Locations:

- `action.yml:87`

### unpinned-uses (severity: high)

Composite steps reference actions by a mutable tag instead of a full commit SHA: line 44 `uses: actions/cache@v3`; line 102 `uses: actions/cache@v3`.

Locations:

- `action.yml:44`
- `action.yml:102`

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

Pinned both actions/cache@v3 uses to 6f8efc29b200d32929f49075959781ed54ec270c (# v3). In the 'Get date' step, inputs.default-packages now comes in through the DEFAULT_PACKAGES env var and is hashed quoted with printf '%s'. The checksum matches upstream's for normal space-separated values; it only feeds a cache key. In the conda create step, default-packages also moves to env. It is split into an array with the quote-aware xargs method (with the unmatched-quote check and the empty-value guard), because upstream pasted the expression straight into the script. ENV_FILE_FLAG is now a bash array, (--file "$ENV_FILE"). PATH is stripped of newlines with printf | tr -d '\n\r' before it is written to GITHUB_ENV. No tests were run on these changes.

