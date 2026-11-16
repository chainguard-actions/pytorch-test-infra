<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261021-234439** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

The 'Calculate docker image' step writes workflow-controlled values to $GITHUB_OUTPUT without first running them through printf '%s' ... | tr -d '\n\r'. These values are DOCKER_IMAGE_NAME (inputs.docker-image-name), DOCKER_TAG (taken from the image name or CUSTOM_TAG_PREFIX), REPO_NAME (inputs.repo-name / github.event.repository.name), DOCKER_REGISTRY (inputs.docker-registry) and CUSTOM_TAG_PREFIX (inputs.custom-tag-prefix or the image name). The affected lines include: echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}", echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}", echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}" and echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}". A newline in any of these values could inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b): the 'Build docker image' step's shell script (nick-fields/retry with.command, run by bash) expands workflow-controlled data without quotes: IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk -F '[:,]' '{print $1}'). DOCKER_IMAGE comes from step outputs built from inputs. The script also runs ${DOCKER_BUILD_SCRIPT} (inputs.docker-build-script) unquoted. Both expansions should be double-quoted, e.g. echo "${DOCKER_IMAGE#...}" and "${DOCKER_BUILD_SCRIPT}".

Locations:

- `action.yml:246`
- `action.yml:248`

### unpinned-uses (severity: high)

A composite step references an action by tag instead of a full 40-character commit SHA: 'uses: nick-fields/retry@v3.0.0'.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

Added a sanitize() helper (printf '%s' | tr -d '\n\r') in the 'Calculate docker image' step and used it on every workflow-controlled value written to GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix). In the 'Build docker image' retry command, double-quoted the DOCKER_IMAGE prefix-strip expansion passed to echo and the DOCKER_BUILD_SCRIPT invocation (it holds a single script path, default ./build.sh). Pinned nick-fields/retry to 7152eba30c6575329ac0576536151aca5a72780e # v3.0.0.

