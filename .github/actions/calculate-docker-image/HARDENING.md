<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261029-163400** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' (id: calculate-image) writes values that come from workflow-controlled sources to $GITHUB_OUTPUT without the `printf '%s' ... | tr -d '\n\r'` sanitization step. The sources are inputs.docker-image-name, inputs.repo-name or github.event.repository.name, inputs.docker-registry and inputs.custom-tag-prefix. The writes are: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"` (lines 95 and 106), `echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"`, where DOCKER_TAG is taken from DOCKER_IMAGE_NAME or CUSTOM_TAG_PREFIX (lines 105 and 118), `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"` (line 119) and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}"` (line 120). A value containing a newline could inject extra step outputs.

Locations:

- `action.yml:95`
- `action.yml:106`
- `action.yml:119`
- `action.yml:120`

### unpinned-uses (severity: high)

A composite step pins an action to a version tag instead of a full commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:237`

### script-injection (severity: high)

Rule (b), unquoted expansion of workflow-controlled data. Step 'Build docker image' passes a bash script to nick-fields/retry as `command:`, and that script expands env vars without quotes. DOCKER_IMAGE comes from steps.calculate-image.outputs.docker-image, which is built from inputs. Line 249: `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk -F '[:,]' '{print $1}')`. DOCKER_BUILD_SCRIPT comes from inputs.docker-build-script and is expanded unquoted as a command on line 251: `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}${CUSTOM_TAG_PREFIX:+:${CUSTOM_TAG_PREFIX}}" -t "${DOCKER_IMAGE}"`.

Locations:

- `action.yml:249`
- `action.yml:251`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses, script-injection

**Notes:**

Pinned nick-fields/retry to 7152eba30c6575329ac0576536151aca5a72780e (v3.0.0). Added a sanitize() helper (printf '%s' | tr -d '\n\r') in the calculate-image step and used it for every write of docker-image, docker-tag and custom-tag-prefix to $GITHUB_OUTPUT. The helper only wraps plain variables, never a command that can fail, so no error gets hidden. In the Build docker image retry command, the DOCKER_IMAGE prefix-strip expansion is now quoted (printf '%s\n' replaces echo). DOCKER_BUILD_SCRIPT is now assigned unquoted into a bash array, which splits and globs it exactly as upstream's unquoted expansion did, and the array is run as "${BUILD_CMD[@]}". I haven't run or tested the edited action.

