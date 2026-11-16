<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-binary-upload/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-binary-upload/v20261103-202628** was hardened automatically. 2 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps use tag refs instead of full 40-character commit SHAs: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:36`
- `action.yml:61`

### github-env-injection (severity: high)

Step 'Set the artifact name' writes values built from inputs.repository, inputs.ref, inputs.python-version, inputs.cuda-version and inputs.arch to $GITHUB_ENV. These pass through env vars REPOSITORY, REF, PYTHON_VERSION, CU_VERSION and ARCH. Nothing removes newlines first (no printf '%s' ... | tr -d '\n\r'): echo "ARTIFACT_NAME=${REPOSITORY//\//_}_${REF//\//_}_${SHORT_PYTHON_VERSION}_${CU_VERSION}_${ARCH}" >> "${GITHUB_ENV}". A newline in any of these inputs could add extra environment variables for later steps.

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

Both findings are fixed in action.yml. I haven't run the action to test it.

- **unpinned-uses:** `actions/setup-python@v5` is now pinned to commit a26af69be951a213d495a4c3e4e4022e16d87065 and `actions/checkout@v4` to commit 11d5960a326750d5838078e36cf38b85af677262. Both SHAs came from lookup_action_sha, and each line keeps a `# v5` or `# v4` comment.
- **github-env-injection:** the 'Set the artifact name' step now builds ARTIFACT_NAME in a shell variable first. It strips newlines from it with `printf '%s' | tr -d '\n\r'` and only then writes it to $GITHUB_ENV. The resulting name is unchanged.

### Iteration 2

**Fixes applied:** github-env-injection

**Notes:**

In action.yml, BUILD_ENV_FILE is now cleaned with `printf '%s' | tr -d '\n\r'` right before it is written to $GITHUB_ENV, and the cleaned value is what gets written. Nothing else changed. Since the step's shell is bash, pipefail is on and this doesn't hide errors.

