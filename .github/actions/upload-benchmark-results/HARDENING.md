<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Two composite steps in action.yml point at a branch instead of a full 40-character commit SHA: 'uses: pytorch/test-infra/.github/actions/setup-uv@main' and 'uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main'. Whoever controls that branch can change the code these steps run.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes 'echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV'. RUNNER_TEMP comes from the process environment this composite action inherits; the script reads it rather than computing it. Nothing strips newlines before the write (no printf '%s' ... | tr -d '\n\r'), so the check's rule for inherited env vars applies. The runner normally sets RUNNER_TEMP itself, so the real-world risk is low, but the check's criterion is not met.

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

- unpinned-uses: The setup-uv and get-workflow-job-id steps used to point at @main. Both now point at pytorch/test-infra@9206d491d3a5507163cb9d5b77040d4c3ef5e038 with a '# main (v20261027-001733)' comment. I checked with lookup_action_sha that this commit exists. It is the upstream commit this action version was built from, so the two sub-actions run at the same snapshot as the action itself. The current tip of main is a different, newer commit (d50cbade).
- github-env-injection: In 'Install dependencies', the VIRTUAL_ENV value now goes through printf '%s' | tr -d '\n\r' before it is written to $GITHUB_ENV, and $GITHUB_ENV is now quoted.

Nothing else in the action was changed. The DEVICE_NAME and DEVICE_TYPE writes to $GITHUB_ENV were not flagged, so I left them as they were. DEVICE_TYPE comes from command output and is not stripped of newlines.

