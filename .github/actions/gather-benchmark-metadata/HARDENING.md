<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite step references an action by branch, not a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a) broken: the 'Gather the metadata' step puts an expression straight into the run: script. Offending lines: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. Whoever calls the action can set inputs.venv to a value with shell metacharacters, and that text runs as shell code. Fix: add `VENV: ${{ inputs.venv }}` to the step's env: block and use "$VENV" in quotes in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the metadata"; move to env: map

Locations:

- `action.yml:57`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the metadata"; move to env: map

Locations:

- `action.yml:58`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

I fixed all four findings in action.yml.

1. **Unpinned action (line 38):** `pytorch/test-infra/.github/actions/get-workflow-job-id@main` now points to the full commit SHA `6f7274a0eff04dd4f8ada574e4e144610cece2c8`, with a `# main` comment so the original ref stays readable. I didn't look up the current SHA of `main`. I used the upstream commit from the request instead, which is the commit this mirror version was built from, so the sub-action matches the rest of the code.

2. **Script injection (lines 57-58):** I added `VENV: ${{ inputs.venv }}` to the env: block of the 'Gather the metadata' step. The script now uses `"${VENV}"` in quotes instead of the inline expression. This fixes both the script-injection finding and the two static-inline-injection findings.

I haven't run anything to test the changes.

