<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20260922-155642** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps pin actions to mutable tags, not 40-char commit SHAs: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66).

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a) is violated in step 'Get latest viable commit'. A ${{ }} expression is put straight into the run script: '--required-checks "${{ inputs.requires }}" \'. The caller controls inputs.requires, and the value is pasted into the bash script before the shell runs it. It should be passed through an env: variable and expanded as "$REQUIRES".

Locations:

- `action.yml:94`

### github-env-injection (severity: high)

Step 'Get latest viable commit' writes '$output' to GITHUB_OUTPUT without cleaning it first: 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output is the result of a script that receives the untrusted inputs.requires value and data fetched from ClickHouse. Before the write, it needs the step printf '%s' "$output" | tr -d '\n\r'.

Locations:

- `action.yml:97`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python to a26af69be951a213d495a4c3e4e4022e16d87065 (# v5) and actions/checkout to 11d5960a326750d5838078e36cf38b85af677262 (# v4). Moved inputs.requires into env REQUIRES and passed it to the script as "$REQUIRES". The script path is now quoted. Newlines and carriage returns are stripped from $output before it is written to GITHUB_OUTPUT. The output is captured on its own line first, so set -e still stops the step if the script fails. I also made one change outside the findings: the push_result heredoc used the fixed delimiter EOF, and now uses a random delimiter read from /dev/urandom. Nothing was run to test these changes.

