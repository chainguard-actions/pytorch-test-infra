<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261103-202628** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): the expression ${{ inputs.venv }} is placed directly into the 'Gather the metadata' run: script, in `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. GitHub substitutes the value into the script text before bash runs it, so a crafted venv value can break out of the quotes and run arbitrary commands. Fix: pass it through env (e.g. VENV: ${{ inputs.venv }}) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

A composite step references an action by a mutable branch ref instead of a full commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

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

I fixed all four findings, which cover three issues, in action.yml. Nothing has been run or tested yet.

- **Script injection (script-injection and both static-inline-injection findings):** The 'Gather the metadata' step pasted `${{ inputs.venv }}` straight into its shell script. The value now goes through the step's env: block as `VENV`, and the script reads it as "${VENV}".
- **Unpinned action (unpinned-uses):** `pytorch/test-infra/.github/actions/get-workflow-job-id` was referenced by `@main`. It is now pinned to commit e9b5b0a4c36ebfde49dec880ae77705038009471 with a `# main` comment. That is the commit this action was built from, as given in the request (same repository). I did not look up where `main` points today. Upstream's `@main` always picked up the latest version, so this pin fixes the sub-action at that commit.

