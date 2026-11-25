<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-232755

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261109-232755** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml points a composite step at a branch, not a commit SHA: 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. Pin it to a full 40-character commit SHA.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a): the 'Gather the metadata' step puts an expression straight into the run: script: 'if [[ -n "${{ inputs.venv }}" ]]; then' and 'source "${{ inputs.venv }}"'. The template is filled in before the shell parses the script, so a crafted venv input can run commands. Move inputs.venv into an env: variable (e.g. VENV) and use "$VENV" in the script.

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

I fixed both findings in action.yml.

- **Unpinned action:** `pytorch/test-infra/.github/actions/get-workflow-job-id@main` is now pinned to commit `2b58f4db8fb1a4e9ed91bd3bd29d16ec00c3de1f` (tag `v20261109-232755`). A lookup confirmed the tag points at that commit, which is also the upstream commit this mirror version was built from.
- **Script injection:** in the 'Gather the metadata' step, `inputs.venv` now goes through a new `VENV` entry in the step's `env:` block. The script uses `"${VENV}"` instead of putting the expression straight into the `run:` text, and it still behaves as before: it only sources the file when `venv` is set.

