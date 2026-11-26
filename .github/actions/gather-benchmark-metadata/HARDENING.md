<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261118-220128** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) is violated: the expression ${{ inputs.venv }} is placed directly inside the run: script of the 'Gather the metadata' step. The offending lines are `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before bash runs, so a crafted venv input can inject shell commands. To fix it, map the input to an env var (VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

Locations:

- `action.yml:59`
- `action.yml:60`

### unpinned-uses (severity: high)

A composite step points to a branch instead of a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:39`

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

I made two changes to action.yml in the 'Gather the metadata' step and the job-id step. First, the step no longer pastes ${{ inputs.venv }} into its script. The input now comes in through a VENV entry in the step's env: block, and the script uses "${VENV}" in both the empty check and the source line. Second, pytorch/test-infra/.github/actions/get-workflow-job-id is now pinned to commit bd1d492a2fc0fbc2310fe4ebc4c4250abdbbf25c (marked '# main'). That is the commit this action version was built from, so the sub-action matches it. pytorch/test-infra's main branch is currently at a1a8f075de6859c2130f960ed710871b5f99ac19. I didn't pin to that because it would bring in newer code than this release used. Nothing has been run to test these changes.

