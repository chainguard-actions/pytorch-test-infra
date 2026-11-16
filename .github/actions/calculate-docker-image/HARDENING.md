<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261112-155209

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261112-155209** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

The 'Calculate docker image' step writes values that come from inputs straight to $GITHUB_OUTPUT. The values are DOCKER_IMAGE_NAME (inputs.docker-image-name), DOCKER_REGISTRY, REPO_NAME (inputs.repo-name / github.event.repository.name), DOCKER_TAG and CUSTOM_TAG_PREFIX, the last two derived from inputs. None of them goes through the required `printf '%s' ... | tr -d '\n\r'` step first. Examples: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"`, `echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"`, `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"` and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}"`. A value containing a newline could inject extra outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b), 'Build docker image' step. The shell `command:` passed to nick-fields/retry expands values from inputs and step outputs without double quotes: `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)` expands DOCKER_IMAGE unquoted, and `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..." -t "${DOCKER_IMAGE}"` expands DOCKER_BUILD_SCRIPT (inputs.docker-build-script) unquoted and runs it as a command.

Locations:

- `action.yml:246`
- `action.yml:248`

### script-injection (severity: high)

Rule (b), 'Check if image should be built' step. The retry helper `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` re-expands its arguments unquoted. One of those arguments is DOCKER_REGISTRY, which comes from inputs.docker-registry, so that value is word-split and glob-expanded. Use "$@" instead.

Locations:

- `action.yml:141`

### script-injection (severity: high)

Rule (b), 'Login to ECR' step. It has the same problem: `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` re-expands DOCKER_REGISTRY (inputs.docker-registry) unquoted. Use "$@" instead.

Locations:

- `action.yml:212`

### unpinned-uses (severity: high)

A composite step points to a version tag instead of a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

action.yml: added a sanitize() helper (printf '%s' | tr -d '\n\r') and now write only sanitized values (docker-image, docker-tag, custom-tag-prefix) to $GITHUB_OUTPUT. The values are captured into variables first and are not nested inside another command substitution. The two retry() helpers now use "$@" in place of $*. In the 'Build docker image' command, DOCKER_IMAGE is quoted (via printf) and DOCKER_BUILD_SCRIPT is invoked quoted. It is a single script path, which the existence check already requires. nick-fields/retry is pinned to 7152eba30c6575329ac0576536151aca5a72780e (v3.0.0).

