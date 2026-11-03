<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261027-001733** was hardened automatically. 6 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an input expression straight into the run: script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The value is substituted into the script before the shell parses it, so the calling workflow can inject shell commands. Fix: pass it through an env: variable and quote it, e.g. printf '%s' "$DEFAULT_PACKAGES".

Locations:

- `action.yml:43`

### script-injection (severity: high)

The 'Setup conda environment with python' step breaks both rules. Rule (a): `${{ inputs.default-packages }} \` is substituted directly into the `conda create` command. Rule (b): `${ENV_FILE_FLAG} \` is expanded without quotes, and it is built from the untrusted input ENV_FILE (`ENV_FILE_FLAG="--file ${ENV_FILE}"`), so the shell will split and glob the value. Fix: pass default-packages through an env: variable and expand it as a bash array or another controlled form. Pass the env file as separate quoted arguments, e.g. `--file "$ENV_FILE"`.

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes the inherited process variable PATH to $GITHUB_ENV without the required sanitization: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside a `{ ... } >> "${GITHUB_ENV}"` block. This script does not set PATH, so the calling workflow controls it. Fix: run printf '%s' ... | tr -d '\n\r' on the value before writing it.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

Two composite steps reference an action by a mutable tag instead of a full 40-character commit SHA: `uses: actions/cache@v3` (Setup miniconda cache) and `uses: actions/cache@v3` (Setup miniconda env cache).

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

Moved inputs.default-packages into env DEFAULT_PACKAGES in both the 'Get date' and 'conda create' steps. Upstream pasted the expression straight into the script, so the value is now split into a bash array with the quote-aware xargs method (with the xargs -r true check for unmatched quotes and an empty-value guard). The checksum is computed over the space-joined array, which gives the same text echo -n produced, so cache keys stay the same. The env file flag is now an array (--file "$ENV_FILE"). PATH is passed through tr -d '\n\r' before it is written to GITHUB_ENV. Both actions/cache@v3 uses are pinned to 6f8efc29b200d32929f49075959781ed54ec270c # v3.

### Iteration 2

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

- unpinned-uses: Both actions/cache@v3 uses are now pinned to 6f8efc29b200d32929f49075959781ed54ec270c # v3. The SHA came from lookup_action_sha.
- github-env-injection: MINICONDA_INSTALL_PATH and CONDA_EXE now go through printf '%s' | tr -d '\n\r' before they are written to GITHUB_PATH or GITHUB_ENV. GITHUB_PATH is now quoted. CONDA_PREFIX and CONDA_RUNTIME get the same treatment before CONDA_ENV, CONDA_PREFIX, CONDA_RUN and CONDA_INSTALL are written.
- Repaired damage from the previous pass: a pin edit had been pasted into the middle of the default-packages split in the 'Get date' step and into a comment. The checksum now hashes the raw input again (printf '%s\n' | md5sum, which gives the same result as upstream's echo).
- Fixed a bug where default packages were never installed: DEFAULT_PKGS was used in the conda create step but never defined there. It is now built in that step with the quote-aware xargs split, because upstream pasted the input expression directly into the script. The empty-value guard and the unmatched-quote check are both in place.

