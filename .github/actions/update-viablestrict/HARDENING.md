<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--update-viablestrict/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--update-viablestrict/v20261103-202628** was hardened automatically. 6 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action references actions by mutable tags instead of full 40-character commit SHAs: 'uses: actions/setup-python@v5' (line 62) and 'uses: actions/checkout@v4' (line 66).

Locations:

- `action.yml:62`
- `action.yml:66`

### script-injection (severity: high)

Rule (a): the 'Get latest viable commit' step puts a GitHub Actions expression straight into the run script: '--required-checks "${{ inputs.requires }}" \'. The workflow supplies this value, and template substitution happens before bash parses the script, so a value containing '"' or '$(...)' can run commands. Move it into an env: variable (e.g. REQUIRES) and use "$REQUIRES". Rule (b): the same step also expands the derived value unquoted with 'echo $output' (line 98).

Locations:

- `action.yml:94`
- `action.yml:98`

### script-injection (severity: high)

Rule (b): the 'Push SHA to viable/strict branch' step expands 'push_result' unquoted with 'echo $push_result'. That variable holds git output that includes the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values. Quote it as "$push_result".

Locations:

- `action.yml:119`

### github-env-injection (severity: high)

'echo "latest_viable_sha=$output" >> "${GITHUB_OUTPUT}"' writes the output of a script whose arguments come from the workflow (inputs.requires) to GITHUB_OUTPUT. Nothing removes newlines first (no printf '%s' ... | tr -d '\n\r'), so the value could inject extra outputs.

Locations:

- `action.yml:97`

### github-env-injection (severity: high)

The push step writes push_result, which is git output containing the workflow-controlled STABLE_BRANCH and LATEST_VIABLE_SHA values, to GITHUB_OUTPUT using a heredoc with the fixed delimiter 'EOF' ('echo push_result<<EOF' / 'echo $push_result' / 'echo EOF' >> "${GITHUB_OUTPUT}"). Nothing sanitizes it first (no printf '%s' ... | tr -d '\n\r'), so a value containing newlines plus 'EOF' could close the heredoc early and inject arbitrary outputs.

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

All changes are in action.yml.
- Pinned the two actions to full commit SHAs: actions/setup-python is now at a26af69be951a213d495a4c3e4e4022e16d87065 (# v5) and actions/checkout at 11d5960a326750d5838078e36cf38b85af677262 (# v4).
- 'Get latest viable commit' step: moved inputs.requires into a REQUIRES env var and pass it as "$REQUIRES". The script path is now quoted. Newlines are stripped from the result before it is written to GITHUB_OUTPUT, and the echo of the result is quoted.
- 'Push SHA to viable/strict' step: the heredoc delimiter is now random for each run (taken from /dev/urandom) instead of the fixed 'EOF', and the value is quoted. Upstream's unquoted echo turned the git output into one line. To keep that, I squeeze runs of whitespace and newlines into single spaces before writing it, so the push_result output stays a single line.

