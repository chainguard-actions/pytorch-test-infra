<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261029-163400

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261029-163400** was hardened automatically. 4 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values taken from inputs to $GITHUB_OUTPUT without first running them through printf '%s' ... | tr -d '\n\r'. The inputs are inputs.docker-image-name, inputs.docker-registry, inputs.repo-name / github.event.repository.name and inputs.custom-tag-prefix. The writes are: echo "docker-image=${DOCKER_IMAGE_NAME}" (lines 92 and 103), echo "docker-tag=${DOCKER_TAG}" (lines 102 and 115; DOCKER_TAG comes from DOCKER_IMAGE_NAME or CUSTOM_TAG_PREFIX), echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" (line 116) and echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" (line 117). A newline inside any of these values lets a caller inject extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b): the helper `retry () { $*  || (sleep 1 && $*) || (sleep 2 && $*) }` expands its arguments unquoted with $*. It is called as `retry login "${DOCKER_REGISTRY}"`, and DOCKER_REGISTRY comes from inputs.docker-registry, so the value is word-split and glob-expanded again. The same code appears in the 'Check if image should be built' step (line 141) and the 'Login to ECR' step (line 212). Use "$@" instead.

Locations:

- `action.yml:141`
- `action.yml:212`

### script-injection (severity: high)

Rule (b): in the 'Build docker image' step, nick-fields/retry runs a bash script from its `command` input. That script contains `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)`. DOCKER_IMAGE comes from step outputs built out of inputs, and it is expanded without double quotes.

Locations:

- `action.yml:246`

### unpinned-uses (severity: high)

A composite step references an action by tag instead of a full commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

I fixed all four findings in action.yml. I haven't run the action to test the changes.

- **Output injection (github-env-injection):** I added a `sanitize()` helper (`printf '%s' | tr -d '\n\r'`) to the 'Calculate docker image' step. Every value it writes to $GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix) now goes through it first. Each value is cleaned from a plain variable, not by wrapping a command, so if a command fails the step still stops as before.
- **Retry helper (script-injection):** In the 'Check if image should be built' and 'Login to ECR' steps, `retry()` now uses "$@" instead of $*. The registry value is no longer split into words or glob-expanded.
- **Image name in the build step (script-injection):** The unquoted `echo ${DOCKER_IMAGE#...}` is now `printf '%s\n' "${DOCKER_IMAGE#...}"`. The text passed to awk is the same as before.
- **Unpinned action (unpinned-uses):** `nick-fields/retry` is now pinned to `7152eba30c6575329ac0576536151aca5a72780e # v3.0.0`. I looked the SHA up with lookup_action_sha rather than guessing it.

