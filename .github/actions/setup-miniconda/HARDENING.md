<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261118-220128** was hardened automatically. 7 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts `${{ inputs.default-packages }}` straight into the run script, unquoted: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. A caller can pass a value containing shell metacharacters and run commands. Fix: pass the input in through an env: variable and quote it ("$DEFAULT_PACKAGES").

Locations:

- `action.yml:43`

### script-injection (severity: high)

Rule (a) and rule (b) in the 'Setup conda environment with python' step. (a) `${{ inputs.default-packages }} \` is placed directly in the conda create command. (b) `${ENV_FILE_FLAG} \` is expanded unquoted. It holds "--file ${ENV_FILE}", which comes from inputs.environment-file. It is a plain string, not an array assignment with a shellcheck directive, so the exemption does not apply. Fix: route default-packages through env: and expand it in a controlled way, and build ENV_FILE_FLAG as a quoted array.

Locations:

- `action.yml:153`
- `action.yml:151`

### script-injection (severity: high)

Rule (b): the 'Install miniconda' step has `case ${RUNNER_OS}-${ARCH} in`. ARCH comes from `${{ steps.arch.outputs.arch }}` and is expanded unquoted in the case word. It should be `case "${RUNNER_OS}-${ARCH}" in`.

Locations:

- `action.yml:74`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step forwards the inherited process env var PATH to $GITHUB_ENV with no sanitization: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside a block redirected to "${GITHUB_ENV}". The calling workflow controls PATH, which is not computed in this script. It needs `printf '%s' "$PATH" | tr -d '\n\r'` before the write.

Locations:

- `action.yml:104`

### unpinned-uses (severity: high)

The composite steps in action.yml reference actions by mutable tag instead of a full commit SHA: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

Locations:

- `action.yml:60`
- `action.yml:119`

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

**Fixes applied:** script-injection, github-env-injection, unpinned-uses, static-inline-injection

**Notes:**

All the findings are fixed, and every change is in action.yml. I haven't run the action to test these changes.

- **Pinned actions:** both uses of actions/cache@v3 now point to the full commit 6f8efc29b200d32929f49075959781ed54ec270c, with a `# v3` comment.
- **Get date step:** `inputs.default-packages` now comes in through an env var (DEFAULT_PACKAGES). The checksum is taken from `printf '%s' "$DEFAULT_PACKAGES"`. For the default value this gives the same checksum as before, so existing cache keys still match. A value with repeated spaces would now give a different checksum, which only affects the cache key.
- **Setup conda env step:** `default-packages` now comes in through an env var. Upstream pasted it straight into the script, so the shell honoured quotes in the value. To keep that behaviour, the value is split with a quote-aware xargs split into an array. The split stops the step on an unmatched quote, and an empty value adds no argument. ENV_FILE_FLAG is now an array, `(--file "$ENV_FILE")`, so the file path stays one argument even if it contains spaces.
- **Install miniconda step:** the case word is now quoted: `case "${RUNNER_OS}-${ARCH}"`.
- **Update path step:** newlines and carriage returns are stripped from PATH before it is written to GITHUB_ENV.

