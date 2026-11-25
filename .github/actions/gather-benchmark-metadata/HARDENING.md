<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) is broken in step 'Gather the metadata'. The input expression ${{ inputs.venv }} is placed straight into the run: script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script before bash runs, so a caller-supplied venv value containing quotes or command substitution would run as shell code. Fix: pass it through env (VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step references an action by branch instead of a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:38`

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

**Fixes applied:** script-injection, static-inline-injection, unpinned-uses

**Notes:**

I moved inputs.venv into the env: block of the 'Gather the metadata' step as VENV. The script now uses "${VENV}" in both the -n check and the source line. I pinned pytorch/test-infra/.github/actions/get-workflow-job-id from @main to the upstream_commit (bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c), which is the commit this action version was built from, and left '# main' as a comment. The current tip of main is d50cbade0e174f113111122f50b7a814b9b4c61d, but I didn't use it because the pin should match this release. I didn't run the action or re-run the analysis to confirm the findings are gone.

