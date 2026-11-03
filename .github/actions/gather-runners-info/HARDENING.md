<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-runners-info/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-runners-info/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), direct expression interpolation: the step 'Gather the runners information' puts `${{ inputs.venv }}` straight into the run: script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script before the shell parses it, so whoever calls the action can inject shell commands (for example a value containing `"; malicious_cmd; "`). Fix: set `VENV: ${{ inputs.venv }}` in the step's env: and use "$VENV" in the script.

Locations:

- `action.yml:73`
- `action.yml:74`

### github-env-injection (severity: high)

The step 'Get device type' writes `echo "DEVICE_TYPE=$DEVICE_TYPE" >> $GITHUB_ENV` without the `printf '%s' ... | tr -d '\n\r'` sanitization step. Which branch sets DEVICE_TYPE depends on the inherited env var DEVICE_NAME. The calling workflow can override that variable through step-level env so that no branch matches, and DEVICE_TYPE is then forwarded from inherited, workflow-controlled env without changes. The rocminfo, hl-smi and nvidia-smi output written in the other branches is not stripped of newlines either. A value containing a newline can add arbitrary environment variables (such as LD_PRELOAD or BASH_ENV). Fix: `safe=$(printf '%s' "$DEVICE_TYPE" | tr -d '\n\r'); echo "DEVICE_TYPE=$safe" >> "$GITHUB_ENV"`.

Locations:

- `action.yml:65`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the runners information"; move to env: map

Locations:

- `action.yml:73`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.venv }}" appears directly in run: block of step "Gather the runners information"; move to env: map

Locations:

- `action.yml:74`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, static-inline-injection, github-env-injection

**Notes:**

I fixed all three findings in action.yml. Nothing was run or tested after the edits.

- **Script injection (both findings, lines 73-74):** the 'Gather the runners information' step no longer pastes `${{ inputs.venv }}` into the script. The value now goes into the step's `env:` as `VENV`, and the script uses "$VENV" in the `-n` check and in `source`.
- **Environment-variable injection:** in 'Get device type', DEVICE_TYPE now has newlines and carriage returns stripped (`printf '%s' "$DEVICE_TYPE" | tr -d '\n\r'`) before it is written. That covers the nvidia-smi, rocminfo, hl-smi and lscpu output as well as a value passed in from the calling workflow.
- **Small extra change:** I put quotes around `$GITHUB_ENV` in the DEVICE_NAME write as well. That value is always one of the script's fixed strings, so it needed nothing more.

