<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261112-155209** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression straight into the run script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. Because inputs.default-packages is substituted into the script text before bash runs, shell metacharacters in it will execute. Fix: pass the value through an env var and quote it, e.g. `printf '%s' "$DEFAULT_PACKAGES" | md5sum`.

Locations:

- `action.yml:42`

### script-injection (severity: high)

Rule (a): the 'Setup conda environment with python' step puts `${{ inputs.default-packages }} \` directly inside the `conda create` command in its run script. Rule (b): the same step expands `${ENV_FILE_FLAG} \` unquoted, and that variable is built from the input-controlled ENV_FILE (`ENV_FILE_FLAG="--file ${ENV_FILE}"`). Fix: move default-packages into an env var. Turn it into an array under a shellcheck SC2206 disable directive, or quote it. Pass the env file as separate quoted arguments, e.g. `--file "$ENV_FILE"`.

Locations:

- `action.yml:134`
- `action.yml:135`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes the inherited process env var PATH to $GITHUB_ENV without sanitizing it first: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` is part of a block redirected to `>> "${GITHUB_ENV}"`. The calling workflow controls PATH, and no `printf '%s' ... | tr -d '\n\r'` step runs before the write, so a value containing newlines could inject extra environment variables.

Locations:

- `action.yml:82`

### unpinned-uses (severity: high)

action.yml references actions by mutable tag instead of a full commit SHA: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

Locations:

- `action.yml:46`
- `action.yml:98`

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

All findings are fixed in action.yml. Nothing was run to test it.

- **default-packages (injection):** both steps that used inputs.default-packages now get it through a DEFAULT_PACKAGES env var instead of having it pasted into the script. Upstream pasted the value straight into the script, so the shell honoured quotes in it. To keep that splitting, the value is split into a bash array with the quote-aware xargs method, which also fails the step on an unmatched quote. The checksum step hashes the split words joined by single spaces. That is what upstream's `echo -n` produced, so existing cache keys should stay the same.
- **environment-file flag:** this is now a bash array, `(--file "$ENV_FILE")`, so the file path is passed as its own quoted argument.
- **PATH written to GITHUB_ENV:** newlines and carriage returns are now stripped from the value before it is written.
- **actions/cache:** both uses are pinned to 6f8efc29b200d32929f49075959781ed54ec270c (# v3).

