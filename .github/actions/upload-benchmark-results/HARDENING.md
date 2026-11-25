<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--upload-benchmark-results/v20261027-001733** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml has composite steps that pin actions to a mutable branch instead of a full 40-character commit SHA: line 31 `uses: pytorch/test-infra/.github/actions/setup-uv@main` and line 115 `uses: pytorch/test-infra/.github/actions/get-workflow-job-id@main`.

Locations:

- `action.yml:31`
- `action.yml:115`

### github-env-injection (severity: high)

The 'Install dependencies' step writes `echo "VIRTUAL_ENV=${RUNNER_TEMP}/benchmark-upload-venv" >> $GITHUB_ENV`. RUNNER_TEMP is an inherited process env var that the script reads but does not set. This check treats any such var in a composite action as untrusted. It is written to $GITHUB_ENV without first running it through `printf '%s' ... | tr -d '\n\r'`. The fix is to sanitize the value into a local variable and write that to "$GITHUB_ENV".

Locations:

- `action.yml:41`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed both findings in action.yml.

- unpinned-uses: the two sub-actions (setup-uv and get-workflow-job-id) were on @main. They are now pinned to 9206d491d3a5507163cb9d5b77040d4c3ef5e038, the upstream commit this mirror version was built from, with a '# main' comment. That keeps them in step with the rest of the action. Current main (058f82ec7cd2fb6cbe66f44cccd28a8c8861b072) was not used.
- github-env-injection: in the 'Install dependencies' step, the VIRTUAL_ENV value is now passed through printf '%s' ... | tr -d '\n\r' before it is written to "$GITHUB_ENV", and $GITHUB_ENV is now quoted.

Nothing was run to test these changes.

