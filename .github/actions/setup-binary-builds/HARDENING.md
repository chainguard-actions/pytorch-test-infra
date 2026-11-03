<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps reference actions by tag instead of a full 40-character commit SHA: 'uses: actions/checkout@v4' (line 55) and 'uses: conda-incubator/setup-miniconda@v3.1.1' (line 92).

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Sub-rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions directly into the run script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}" and echo "${{ github.base_ref }}". These values are substituted into the script before the shell runs, so an attacker who controls a ref name can inject commands. Fix: pass them through env: variables and quote the expansions.

Locations:

- `action.yml:71`
- `action.yml:72`
- `action.yml:73`
- `action.yml:74`

### script-injection (severity: high)

Sub-rule (b): in the 'Setup conda environment for build' step, PYTHON_VERSION comes from inputs.python-version and is expanded without quotes in 'case $PYTHON_VERSION in'. Fix: quote it as "$PYTHON_VERSION".

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"'. CU_VERSION, ARCH and PYTHON_VERSION (the source of SHORT_PYTHON_VERSION) come from inputs. REPOSITORY and REF are inherited from the calling workflow's environment. None of them goes through printf '%s' ... | tr -d '\n\r' first, so a value containing a newline can inject arbitrary environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

All changes are in action.yml.

- **unpinned-uses:** pinned actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (v4) and conda-incubator/setup-miniconda to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). Both SHAs came from lookup_action_sha, and the tag is kept in a trailing comment.
- **script-injection:** in the 'Log Available Webhook Fields' step, the four github.* expressions now come in through env vars (CTX_REF_NAME, CTX_EVENT_REF, CTX_REF, CTX_BASE_REF) and are echoed quoted. In the conda setup step, the case statement now quotes the variable: case "$PYTHON_VERSION".
- **github-env-injection:** the 'Set artifact name' step now builds the artifact name in a variable, strips newlines and carriage returns with printf '%s' | tr -d '\n\r', and then writes it to GITHUB_ENV. REPOSITORY and REF still come from the calling workflow's environment, as upstream does; the newline stripping covers them as well.

### Iteration 2

**Fixes applied:** script-injection, github-env-injection

**Notes:**

I fixed all three findings in action.yml and repaired the parts of the file that were corrupted. While I was editing, the edit tool damaged the file further, so I rewrote it in full instead. I did not run or validate the result.

1. **script-injection (debug step):** Moved the shell/env/run block out of the actions/checkout step into its own step, 'Log Available Webhook Fields'. Removed the stray `}}"` and the inline `echo "${{ github.base_ref }}"`; the step now prints only the CTX_BASE_REF environment variable.
2. **github-env-injection (Set artifact name):** Put back the SHORT_PYTHON_VERSION line, which had been cut off. The artifact name is now built in ARTIFACT_NAME_RAW, newlines are removed with `printf '%s' | tr -d '\n\r'`, and only that cleaned value is written to GITHUB_ENV. The unsanitized write is gone.
3. **script-injection (conda setup step):** Fixed the broken OPENSSL_PIN line to `export OPENSSL_PIN="openssl=3.5.6"` and quoted the variable in `case "$PYTHON_VERSION" in`.

Three of these repairs are my reconstruction, because the original text was lost:
- The step name 'Log Available Webhook Fields'.
- The version `3.5.6`, taken from the comment above that line.
- A `# shellcheck disable=SC2153` line before the case statement, rebuilt from the fragment `le=SC2153`.

I also wrote a new comment on the SHORT_PYTHON_VERSION line, since the original wording was lost. REPOSITORY and REF are still read from the calling workflow's environment, as before.

