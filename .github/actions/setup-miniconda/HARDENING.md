<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-miniconda/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-miniconda/v20261027-001733** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the 'Get date' step puts an expression straight into the run: script: `echo "default_packages_checksum=$(echo -n ${{ inputs.default-packages }} | md5sum | awk '{print $1}' )" >> "${GITHUB_OUTPUT}"`. The value of inputs.default-packages is pasted into the script before the shell runs, so shell metacharacters in it would execute as commands. Fix: pass it through an env: variable and use "$DEFAULT_PACKAGES" in the script.

Locations:

- `action.yml:43`

### script-injection (severity: high)

The 'Setup conda environment with python' step breaks two rules. Rule (a): `${{ inputs.default-packages }} \` is interpolated directly into the conda create command. Rule (b): ENV_FILE_FLAG is built from the input-derived ENV_FILE (`ENV_FILE_FLAG="--file ${ENV_FILE}"`) and then expanded unquoted (`${ENV_FILE_FLAG} \`). Fix: route default-packages through env: and turn it into an array (e.g. `# shellcheck disable=SC2206` followed by PKGS=($DEFAULT_PACKAGES)). Build the env-file flag as an array too, e.g. ENV_FILE_ARGS=(--file "$ENV_FILE"), and expand it as "${ENV_FILE_ARGS[@]}".

Locations:

- `action.yml:139`
- `action.yml:137`

### github-env-injection (severity: high)

The 'Update GitHub path to include miniconda install' step writes the inherited process env var PATH to $GITHUB_ENV without sanitizing it: `echo "PATH=${MINICONDA_INSTALL_PATH}/bin:${PATH}"` inside `{ ... } >> "${GITHUB_ENV}"`. In a composite action the calling workflow controls PATH, and the value is not passed through `printf '%s' ... | tr -d '\n\r'` before the write. A newline in it could inject extra environment variables.

Locations:

- `action.yml:90`

### unpinned-uses (severity: high)

action.yml uses composite action steps pinned to a mutable tag instead of a 40-character commit SHA: `uses: actions/cache@v3` (line 47, 'Setup miniconda cache') and `uses: actions/cache@v3` (line 105, 'Setup miniconda env cache').

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

**Fixes applied:** script-injection, github-env-injection, unpinned-uses, static-inline-injection

**Notes:**

I fixed all six findings in action.yml.

- **Pinned actions:** both actions/cache@v3 references now point to commit 6f8efc29b200d32929f49075959781ed54ec270c, with a `# v3` comment.
- **default-packages input:** in both affected steps the value now comes in through an env var (DEFAULT_PACKAGES) instead of being pasted into the script. Upstream pasted it straight into the script, so the shell honoured quotes in it. To keep that behaviour, I split it into an array with the quote-aware xargs method (guarded for empty values, and it fails on an unmatched quote). The checksum is still computed from `echo -n` of the same words, so cache keys for normal values don't change. The `conda create` call uses `"${PKGS[@]}"`. One small difference: upstream's version also expanded glob characters like `*` in package names against files; the new split passes them to conda as plain text.
- **Env-file flag:** this is now built as an array, `ENV_FILE_ARGS=(--file "$ENV_FILE")`, and passed as `"${ENV_FILE_ARGS[@]}"`, so file paths containing spaces stay one argument.
- **PATH written to GITHUB_ENV:** newlines are now stripped with `printf '%s' ... | tr -d '\n\r'` before the value is written.

I haven't run the action to test these changes.

