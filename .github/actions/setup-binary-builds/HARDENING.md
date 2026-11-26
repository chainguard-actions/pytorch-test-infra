<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-builds/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-builds/v20261125-223308** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references actions by mutable tag instead of a full 40-char commit SHA: 'uses: actions/checkout@v4' and 'uses: conda-incubator/setup-miniconda@v3.1.1'.

Locations:

- `action.yml:55`
- `action.yml:92`

### script-injection (severity: high)

Rule (a): the 'Log Available Webhook Fields' step puts GitHub expressions straight into the run script: echo "${{ github.ref_name }}", echo "${{ github.event.ref }}", echo "${{ github.ref }}", echo "${{ github.base_ref }}". Branch and ref names can contain shell metacharacters. Pass these values through env: variables or use the existing $GITHUB_REF_NAME/$GITHUB_REF/$GITHUB_BASE_REF variables instead.

Locations:

- `action.yml:71`

### script-injection (severity: high)

Rule (b): in the 'Setup conda environment for build' step, the input-derived env var is expanded without quotes as a case subject: 'case $PYTHON_VERSION in'. PYTHON_VERSION comes from inputs.python-version. Quote it as "$PYTHON_VERSION".

Locations:

- `action.yml:153`

### github-env-injection (severity: high)

The 'Set artifact name' step writes 'echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}"'. CU_VERSION and ARCH come from inputs. SHORT_PYTHON_VERSION is derived from inputs.python-version, and the sed call does not remove newlines. REPOSITORY and REF are inherited process env vars that this step never sets. None of these values goes through printf '%s' ... | tr -d '\n\r' first, so a newline in any of them could inject extra environment variables.

Locations:

- `action.yml:89`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection

**Notes:**

I fixed all four findings in action.yml. The changes are edits only and I haven't run anything.

- **Unpinned actions:** `actions/checkout` is now pinned to commit 11d5960a326750d5838078e36cf38b85af677262 (v4). `conda-incubator/setup-miniconda` is pinned to 505e6394dae86d6a5c7fbb6e3fb8938e3e863830 (v3.1.1). Both SHAs came from a git lookup and a trailing comment keeps the tag name.
- **Webhook logging step:** the four `${{ github.* }}` values (`ref_name`, `event.ref`, `ref`, `base_ref`) now go through the step's `env:` block. The script echoes them as `$GH_REF_NAME`, `$GH_EVENT_REF`, `$GH_REF` and `$GH_BASE_REF`.
- **Conda environment step:** `case $PYTHON_VERSION in` is now `case "$PYTHON_VERSION" in`.
- **Artifact name step:** the full `ARTIFACT_NAME` value is built first, then passed through `printf '%s' ... | tr -d '\n\r'` before it's written to `$GITHUB_ENV`. The way the name is built is unchanged, including the `REPOSITORY` and `REF` values the step inherits from the environment. The step still fails under `set -u` if either is unset, just as upstream does.

