<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--setup-linux/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--setup-linux/v20261021-234439** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml references a composite step action by a mutable branch instead of a full 40-character commit SHA: `uses: pytorch/test-infra/.github/actions/setup-nvidia@main`. Anyone who can push to that branch can change the code this action runs.

Locations:

- `action.yml:88`

### github-env-injection (severity: high)

The 'Setup useful environment variables' step builds RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR from the inherited process env var ${RUNNER_TEMP}. That variable is not set inside this run: block. The step then writes the values to $GITHUB_ENV without first cleaning them with `printf '%s' ... | tr -d '\n\r'`, e.g. `echo "RUNNER_ARTIFACT_DIR=${RUNNER_ARTIFACT_DIR}" >> "${GITHUB_ENV}"`. In a composite action, inherited env is controlled by the calling workflow, so a value containing a newline could inject extra environment variables.

Locations:

- `action.yml:65`
- `action.yml:70`
- `action.yml:75`

### static-arg-collapse (severity: medium)

argument collapse in step "Set GPU_FLAG if in a container that has a NVIDIA GPU": a flag and its value are stored together in one variable and written to GITHUB_OUTPUT/GITHUB_ENV; when expanded double-quoted they become a single argument and the command never sees the bare flag. Build the command with a bash array (e.g. args=(); [ -n "$VAL" ] && args+=(--flag "$VAL"); cmd "${args[@]}") so each token stays a separate, quoted argument

Locations:

- `action.yml:99`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, github-env-injection

**Notes:**

I fixed two of the three findings in action.yml. I left the third (static-arg-collapse) as it was on purpose, so the next analysis pass may report it again.

- unpinned-uses: pinned pytorch/test-infra/.github/actions/setup-nvidia to 4bb924e6cddf98370d0c754d6769b492fe457233, the commit this mirror was built from, with a '# main' comment. Current main is c91174703a48..., but I used the build commit so the sub-action matches the rest of the action.
- github-env-injection: RUNNER_ARTIFACT_DIR, RUNNER_TEST_RESULTS_DIR and RUNNER_DOCS_DIR now go through printf '%s' ... | tr -d '\n\r' before being written to GITHUB_ENV.
- static-arg-collapse (not fixed): the step writes GPU_FLAG='--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all' to GITHUB_ENV. The flagged collapse would only happen if GPU_FLAG were expanded double-quoted, and nothing in this action does that. GPU_FLAG is part of the action's public interface: calling workflows expand it unquoted (docker run ${GPU_FLAG:-} ...) so it splits into separate docker arguments, and the setup-nvidia sub-action sets the same variable. Splitting it into an array or changing its form would break every consumer, and there is no command in this action to rebuild with an array. I only added a comment saying it must stay unquoted. If the finding comes back, the options are to accept it as a false positive or to deliberately change the GPU_FLAG interface for consumers.

### Iteration 2

**Fixes applied:** static-arg-collapse

**Notes:**

Changed the "Set GPU_FLAG" step so the flag tokens are built as a bash array (gpu_args=(--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all)) and joined only when written to GITHUB_ENV. The exported value is still exactly the same as upstream's ('--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all'). Workflows that use this action expand ${GPU_FLAG} unquoted to split it into docker arguments, so the value had to stay the same. Nothing in this action expands GPU_FLAG double-quoted, and the value is a fixed string with nothing injectable in it, so this finding was mostly a false positive. Not tested: no run was done to confirm the analyzer stops reporting it.

