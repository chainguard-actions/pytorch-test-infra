<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261125-223308

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261125-223308** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite steps use mutable tag refs instead of full commit SHAs: 'uses: actions/setup-python@v5' and 'uses: actions/checkout@v4'.

Locations:

- `action.yml:64`
- `action.yml:68`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts an expression straight into the run script: '--required-checks "${{ inputs.requires }}" \'. The input is substituted into the script before the shell runs, so a value containing a double quote can break out of the quoted string and run commands. Rule (b): the same step also expands '${TEST_INFRA_PATH}' and '$output' without quotes ('python ${TEST_INFRA_PATH}/tools/...', 'echo $output'). Fix: move inputs.requires into an env var (e.g. REQUIRES) and use "$REQUIRES". Quote the other expansions too.

Locations:

- `action.yml:95`

### script-injection (severity: high)

Rule (b): the 'Push SHA to viable/strict branch' step runs 'echo $push_result' with the variable unquoted. push_result holds git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. Use "$push_result".

Locations:

- `action.yml:121`

### github-env-injection (severity: high)

The 'Get latest viable commit' step writes 'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"'. $output is the script's output, and that output depends on the untrusted inputs.requires value. Nothing removes newlines before the write (no printf '%s' ... | tr -d '\n\r'), so extra output lines could be injected.

Locations:

- `action.yml:98`

### github-env-injection (severity: high)

The 'Push SHA to viable/strict branch' step writes push_result to $GITHUB_OUTPUT using a fixed 'EOF' heredoc delimiter, with no sanitization. push_result is git output that includes the input-controlled STABLE_BRANCH and the step-output-derived LATEST_VIABLE_SHA. Newlines or a line reading 'EOF' in that output could end the block early and inject extra outputs. Sanitize the value with printf '%s' ... | tr -d '\n\r' or use a random delimiter.

Locations:

- `action.yml:118`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.requires }}" appears directly in run: block of step "Get latest viable commit"; move to env: map

Locations:

- `action.yml:94`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python to a26af69b… (v5) and actions/checkout to 11d5960a… (v4). Moved inputs.requires into the REQUIRES env var and quoted the TEST_INFRA_PATH, output and push_result expansions. latest_viable_sha now has newlines stripped before it is written to GITHUB_OUTPUT. push_result keeps its heredoc form, but the fixed 'EOF' delimiter is now a random one read from /dev/urandom. Behaviour change: quoting $push_result means the output now keeps git's line breaks. Before, the unquoted echo joined everything onto one line.

