<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261112-155209** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps use mutable tag refs instead of full 40-char commit SHAs: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the step 'Get latest viable commit' puts the expression ${{ inputs.requires }} directly into the run: script: '--required-checks "${{ inputs.requires }}" \'. The value is substituted into the script before bash runs, so a crafted input can break out of the quotes and run commands. Fix: pass it through env (e.g. REQUIRES: ${{ inputs.requires }}) and use "$REQUIRES". The same step also has 'echo $output' unquoted, and output comes from a script fed workflow-controlled input.

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Rule (b): the step 'Push SHA to viable/strict branch' runs 'echo $push_result' with no quotes. push_result holds git push output, which repeats the workflow-controlled STABLE_BRANCH (inputs.stable-branch) and LATEST_VIABLE_SHA values. The expansion must be double-quoted.

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

The step 'Get latest viable commit' writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output comes from a script run with workflow-controlled input (inputs.requires) and is not passed through printf '%s' ... | tr -d '\n\r' first, so a newline in it could inject extra outputs.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The step 'Push SHA to viable/strict branch' writes push_result to $GITHUB_OUTPUT through a fixed 'EOF' heredoc delimiter ('echo push_result<<EOF; echo $push_result; echo EOF' >> "${GITHUB_OUTPUT}"). push_result is git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values, and it is not run through printf '%s' ... | tr -d '\n\r' first. A value containing newlines or the delimiter could inject arbitrary outputs.

Locations:

- `action.yml:117`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python and actions/checkout to full commit SHAs. Moved inputs.requires into env (REQUIRES) and quoted it, quoted the script path and echo of output. Stripped newlines from output before writing latest_viable_sha to GITHUB_OUTPUT. Replaced the fixed EOF heredoc delimiter for push_result with a random per-run delimiter from /dev/urandom, and quoted push_result expansion.

