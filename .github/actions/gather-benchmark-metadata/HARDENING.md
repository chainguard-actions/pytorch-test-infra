<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261027-001733** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step pins a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Whoever controls that branch can change the code this action runs.

Locations:

- `action.yml:38`

### script-injection (severity: high)

Rule (a), direct expression interpolation. In the 'Gather the metadata' step, `${{ inputs.venv }}` is placed straight into the run: script: `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before the shell parses it, so a crafted input can break out of the quotes and run commands. Fix: pass it through env (e.g. `VENV: ${{ inputs.venv }}`) and use `"$VENV"` in the script.

Locations:

- `action.yml:58`
- `action.yml:59`

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

Changed the get-workflow-job-id step so it uses pytorch/test-infra/.github/actions/get-workflow-job-id at commit 9206d491d3a5507163cb9d5b77040d4c3ef5e038 instead of the main branch. That is the upstream commit this version was built from, and lookup_action_sha confirmed it resolves. In the 'Gather the metadata' step, inputs.venv now goes through the env: block as VENV, and the script reads it as "${VENV}". Nothing was tested or run. Possible problem I noticed but didn't fix: the step runs ${GITHUB_ACTION_PATH}/../../scripts/benchmarks/gather_metadata.py, and the hardened directory contains only action.yml. If the mirror doesn't include upstream's scripts/ directory, that step will fail at runtime.

