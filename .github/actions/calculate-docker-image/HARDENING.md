<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261112-155209** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values taken from inputs to $GITHUB_OUTPUT without first passing them through printf '%s' ... | tr -d '\n\r'. The inputs are docker-image-name, docker-registry, repo-name (or github.event.repository.name) and custom-tag-prefix, read through the env vars DOCKER_IMAGE_NAME, DOCKER_REGISTRY, REPO_NAME and CUSTOM_TAG_PREFIX. The writes are: echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"; echo "docker-tag=${DOCKER_TAG}" (DOCKER_TAG comes from the image name or the custom tag prefix); echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"; and echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}". A value containing a newline can add arbitrary step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b): workflow-controlled data is expanded without quotes. In the steps 'Check if image should be built' and 'Login to ECR', the retry helper runs `$*  || (sleep 1 && $*) || (sleep 2 && $*)` with the arguments login "${DOCKER_REGISTRY}". DOCKER_REGISTRY comes from inputs.docker-registry, and the unquoted $* re-splits it and expands globs. Use "$@" instead. In the 'Build docker image' step, the bash command passed to nick-fields/retry contains `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)`, which leaves the input-derived DOCKER_IMAGE expansion unquoted.

Locations:

- `action.yml:141`
- `action.yml:212`
- `action.yml:246`

### unpinned-uses (severity: high)

A composite step uses an action by mutable tag instead of a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

I fixed all three findings in action.yml. I haven't run the action, so none of these changes have been tested.

- **Step outputs (github-env-injection):** the 'Calculate docker image' step now has a small `sanitize()` helper that runs `printf '%s' "$1" | tr -d '\n\r'`. Every value written to $GITHUB_OUTPUT that comes from an input (docker-image, docker-tag, custom-tag-prefix) now goes through it first. The helper is only ever given plain variables, never a command's output, so a failing command still stops the step under `set -e`.
- **Unquoted values (script-injection):** the retry helper in 'Check if image should be built' and 'Login to ECR' now uses `"$@"` instead of `$*`, so the registry value is no longer re-split or treated as a glob pattern. In 'Build docker image', IMAGE_NAME is now built with `printf '%s\n' "${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"}"`, so DOCKER_IMAGE is quoted. The prefix-stripping logic is the same as before.
- **Unpinned action:** `nick-fields/retry@v3.0.0` is now pinned to its commit, `7152eba30c6575329ac0576536151aca5a72780e # v3.0.0`.

