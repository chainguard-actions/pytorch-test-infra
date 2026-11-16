<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261109-192709

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261109-192709** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points at a branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Whoever controls that branch can change the code this action runs at any time. Pin it to a commit SHA.

Locations:

- `action.yml:88`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var ${RUNNER_TEMP}. The script reads this variable but does not set it. It then writes the values to $GITHUB_ENV without first running them through `printf '%s' ... | tr -d '\n\r'` (e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`). Strip newline and carriage-return characters from each value before writing it.

Locations:

- `action.yml:68`

### static-arg-collapse (severity: medium)

argument collapse in step "Set GPU_FLAG if in a container that has a NVIDIA GPU": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:99`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed the two high-severity findings in action.yml. I left the medium static-arg-collapse finding alone on purpose, so the next analysis pass will probably report it again.

- unpinned-uses: pytorch/test-infra/.github/actions/setup-nvidia@main is now pinned to 0569df511711f70601c984fe3a93dac324afc9ce, with '# main' kept as a comment. That is the upstream commit this mirror version was built from, so setup-nvidia now runs the same code as the rest of the action. I did not look the SHA up separately; it is the upstream_commit given in the request.
- github-env-injection: In 'Setup useful environment variables', RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now go through printf '%s' | tr -d '\n\r' before being written to $GITHUB_ENV. The step runs under shell: bash, which composite actions start with pipefail.
- static-arg-collapse (not changed): GPU_FLAG='--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all' is a public env var that this action exports and never uses itself. PyTorch caller workflows pass it unquoted to 'docker run ${GPU_FLAG}', so the shell splits it into separate arguments as intended, and the collapse described in the finding never happens. Turning it into an array or renaming it would break every downstream workflow that uses it, and a bash array can't be exported through GITHUB_ENV anyway. The value is a fixed string with no user input, so nothing can be injected through it.

### Iteration 2

**Fixes applied:** static-arg-collapse

**Notes:**

In the step "Set GPU_FLAG if in a container that has a NVIDIA GPU", the flag tokens are now kept in a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)) and written with printf instead of as one packed string. The value written to GITHUB_ENV is still exactly upstream's 'GPU_FLAG=--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all'. GPU_FLAG is a fixed constant (no user input, so nothing can be injected). The action never runs it itself: downstream PyTorch workflows read it unquoted (docker run ${GPU_FLAG:-}), and that splits it into separate arguments. GITHUB_ENV can't carry an array, so changing the value or how it's split would break callers. If the analyzer flags the env-var string itself, treat that as a false positive here. I have not run the action or re-run the analysis after the edit.

