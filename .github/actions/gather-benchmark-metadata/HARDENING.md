<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--gather-benchmark-metadata/v20261112-155209** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a), direct expression interpolation: in the 'Gather the metadata' step, `${{ inputs.venv }}` is placed straight into the run: script, in the lines `if [[ -n "${{ inputs.venv }}" ]]; then` and `source "${{ inputs.venv }}"`. The value is substituted into the script text before bash parses it, so a crafted venv input could run arbitrary commands. Fix: pass it through env (e.g. `VENV: ${{ inputs.venv }}`) and use "$VENV" in the script.

Locations:

- `action.yml:57`
- `action.yml:58`

### unpinned-uses (severity: high)

The composite step refers to an action by a mutable branch instead of a commit SHA: `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`. Pin it to a full 40-character commit SHA.

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

In hardened/action/action.yml, the 'Gather the metadata' step no longer puts inputs.venv straight into its run: script. The value is now passed in through a new VENV entry in the step's env: block, and the script checks and sources it as "${VENV}". The sub-action pytorch/test-infra/.github/actions/get-workflow-job-id was referenced by the main branch. It is now pinned to 6f7274a0eff04dd4f8ada574e4e144610cece2c8 # main. That is the upstream commit this version was built from, so the job-id sub-action matches the rest of this release instead of whatever main points to today. lookup_action_sha confirmed the commit exists in pytorch/test-infra. I made no other changes and have not run the action.

