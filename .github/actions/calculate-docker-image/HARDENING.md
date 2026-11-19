<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261118-220128

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261118-220128** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values derived from untrusted inputs to $GITHUB_OUTPUT with no `printf '%s' ... | tr -d '\n\r'` sanitization. DOCKER_IMAGE_NAME (inputs.docker-image-name), DOCKER_REGISTRY (inputs.docker-registry), REPO_NAME (inputs.repo-name / github.event.repository.name), CUSTOM_TAG_PREFIX (inputs.custom-tag-prefix) and DOCKER_TAG, which is derived from them, are all written this way. Examples: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"`, `echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"`, `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"`, `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}"`. A value containing a newline could inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### unpinned-uses (severity: high)

A composite step uses an action pinned to a tag instead of a full commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

### script-injection (severity: high)

Rule (b): the 'Build docker image' step runs its shell script through nick-fields/retry `command:`, and that script expands workflow-controlled data without quotes: `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk -F '[:,]' '{print $1}')`. DOCKER_IMAGE comes from steps.calculate-image.outputs.docker-image, which is built from inputs. The expansion should be double-quoted.

Locations:

- `action.yml:246`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses, script-injection

**Notes:**

Fixed all three findings in action.yml.

- github-env-injection: the 'Calculate docker image' step now has a sanitize() helper (printf '%s' | tr -d '\n\r'). Every value written to GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix) goes through it and is stored in a separate SAFE_* variable before being written. The command substitution is a plain assignment, not nested inside another call, and the original variables that the script compares against are left as they were.

- unpinned-uses: nick-fields/retry is now pinned to 7152eba30c6575329ac0576536151aca5a72780e # v3.0.0. I got the SHA from lookup_action_sha.

- script-injection: the line in the retry command that strips the prefix from DOCKER_IMAGE now quotes the expansion: echo "${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"}" | awk. A docker image reference is a single value, so quoting it doesn't change how it behaves.

