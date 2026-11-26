<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261125-223308** was hardened automatically. 7 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): an expression is placed straight into the run: script in the 'Get date' step: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum ...)" >> "${GITHUB_OUTPUT}"`. Whoever calls the action controls inputs.default-packages, so they can inject shell commands. Fix: pass the value in through an env: variable and quote it when the script uses it.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a): an expression is placed straight into the run: script in the 'Setup conda environment with python' step: `${{ inputs.default-packages }} \` inside the conda create command. Rule (b): `${ENV_FILE_FLAG} \` is unquoted, and ENV_FILE_FLAG holds the caller-controlled inputs.environment-file value (`ENV_FILE_FLAG="--file ${ENV_FILE}"`).

Locations:

- `action.yml:152`
- `action.yml:150`

### script-injection (severity: high)

Rule (b): an unquoted expansion of workflow-controlled data in the 'Install miniconda' step: `case ${RUNNER_OS}-${ARCH} in`. ARCH comes from steps.arch.outputs.arch. Quote it as "${RUNNER_OS}-${ARCH}".

Locations:

- `action.yml:74`

### unpinned-uses (severity: high)

Composite steps use tag refs instead of full commit SHAs: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

Locations:

- `action.yml:60`
- `action.yml:118`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step forwards the inherited PATH env var to $GITHUB_ENV without sanitizing it: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` is written to "${GITHUB_ENV}". The calling workflow controls PATH, so a newline in it could inject extra environment variables. Run it through printf '%s' "$PATH" | tr -d '\n\r' before the write.

Locations:

- `action.yml:103`

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

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses, github-env-injection

**Notes:**

I fixed everything in action.yml.
- inputs.default-packages now reaches both steps that use it ('Get date' and 'Setup conda environment') through an env var instead of being written into the script. Upstream pasted it straight in, so the shell honoured quotes in the value. To split it the same way, I use the quote-aware xargs pattern: guarded for an empty value, with an `xargs -r true` check that fails on an unmatched quote. In 'Get date' the checksum is now `echo -n "${pkgs[@]}"` and conda create gets `"${pkgs[@]}"`.
- ENV_FILE_FLAG is now a bash array (--file "$ENV_FILE"), expanded quoted.
- The case statement now quotes "${RUNNER_OS}-${ARCH}".
- Both actions/cache@v3 steps are pinned to 6f8efc29b200d32929f49075959781ed54ec270c # v3.
- The PATH value written to GITHUB_ENV now has newlines and carriage returns removed with tr first.
Nothing was run or tested.

