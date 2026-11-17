<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261021-234439

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261021-234439** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

The 'Calculate docker image' step writes values that come from workflow inputs to $GITHUB_OUTPUT without first running them through printf '%s' ... | tr -d '\n\r'. The affected lines are echo "docker-image=${DOCKER_IMAGE_NAME}", echo "docker-tag=${DOCKER_TAG}" (the tag is taken from the image name or the custom-tag-prefix input), echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" and echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}". These variables are set from inputs.docker-image-name, inputs.docker-registry, inputs.repo-name / github.event.repository.name and inputs.custom-tag-prefix. A value containing a newline can inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:100`
- `action.yml:101`
- `action.yml:116`
- `action.yml:117`
- `action.yml:118`

### script-injection (severity: high)

Rule (b), unquoted expansion. The 'Check if image should be built' and 'Login to ECR' steps define retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) } and call it as retry login "${DOCKER_REGISTRY}". DOCKER_REGISTRY comes from inputs.docker-registry. Because $* is unquoted, that value is split on whitespace and glob-expanded when it is re-run. Use "$@" instead.

Locations:

- `action.yml:136`
- `action.yml:210`

### unpinned-uses (severity: high)

A composite step uses a version tag instead of a full commit SHA: 'uses: nick-fields/retry@v3.0.0'.

Locations:

- `action.yml:233`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

I fixed all three findings in action.yml.

1. github-env-injection: I added a sanitize() helper to the 'Calculate docker image' step. It runs printf '%s' "$1" | tr -d '\n\r'. Every input-derived value (docker-image, docker-tag, custom-tag-prefix) now goes through it into a SAFE_* variable before being written to $GITHUB_OUTPUT. sanitize only ever receives plain variables, never a nested command substitution, so a failing command still stops the step under set -e as before.

2. script-injection: In both retry() helpers ('Check if image should be built' and 'Login to ECR'), I replaced the unquoted $* with "$@". The registry value is now passed as one argument instead of being split on whitespace and glob-expanded.

3. unpinned-uses: I pinned nick-fields/retry@v3.0.0 to the commit SHA 7152eba30c6575329ac0576536151aca5a72780e, which I looked up rather than guessed, and kept '# v3.0.0' as a comment.

Nothing has been run or tested, and the analysis has not been re-run yet.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

In the 'Build docker image' step (nick-fields/retry command), the IMAGE_NAME computation now uses printf '%s\n' "${DOCKER_IMAGE#...}" (quoted) instead of an unquoted echo, preventing word splitting/globbing. Left ${DOCKER_BUILD_SCRIPT} unquoted as upstream intends it to be split into a command plus arguments.

