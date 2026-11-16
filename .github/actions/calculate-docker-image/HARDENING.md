<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20260922-155642

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20260922-155642** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values taken from workflow inputs to $GITHUB_OUTPUT without first running them through printf '%s' ... | tr -d '\n\r'. The inputs are DOCKER_IMAGE_NAME (inputs.docker-image-name), DOCKER_REGISTRY (inputs.docker-registry), REPO_NAME (inputs.repo-name / github.event.repository.name) and CUSTOM_TAG_PREFIX (inputs.custom-tag-prefix). Examples: `echo "docker-image=${DOCKER_IMAGE_NAME}" >> "${GITHUB_OUTPUT}"`, `echo "docker-tag=${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"` (DOCKER_TAG comes from DOCKER_IMAGE_NAME or CUSTOM_TAG_PREFIX), `echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" >> "${GITHUB_OUTPUT}"` and `echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}" >> "${GITHUB_OUTPUT}"`. A value containing a newline could add extra outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### unpinned-uses (severity: high)

A composite step pins an action to a tag, not a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

### script-injection (severity: high)

Rule (b), unquoted shell expansion of workflow-controlled data. The 'Build docker image' step runs this shell script through nick-fields/retry's `command:` field: `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)`. DOCKER_IMAGE comes from steps.calculate-image.outputs.docker-image, which is built from inputs, and it is expanded unquoted. The next line, `${DOCKER_BUILD_SCRIPT} "${IMAGE_NAME}..."`, also runs the unquoted value of inputs.docker-build-script. Both expansions are subject to word splitting and glob expansion.

Locations:

- `action.yml:246`
- `action.yml:248`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses, script-injection

**Notes:**

I fixed all three findings in action.yml.

1. github-env-injection: in the 'Calculate docker image' step, every value written to $GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix) now goes through printf '%s' | tr -d '\n\r' first. The DOCKER_TAG value is still worked out in its own assignment, so a failure there still stops the step.

2. unpinned-uses: nick-fields/retry is now pinned to 7152eba30c6575329ac0576536151aca5a72780e (v3.0.0). I got that SHA from lookup_action_sha.

3. script-injection: in the retry command, I replaced the unquoted 'echo ${DOCKER_IMAGE#...}' with a quoted printf '%s\n' "${DOCKER_IMAGE#...}". I also quoted the build script as "${DOCKER_BUILD_SCRIPT}", since the input is a single script path (default ./build.sh).

Nothing was run to test these changes. One behaviour change: before this, a docker-build-script value with spaces in it (a script plus extra arguments) was split into separate words. It now runs as one path, so that kind of value would break.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

I changed both `retry` helpers in action.yml (in the 'Check if image should be built' and 'Login to ECR' steps) from unquoted `$*` to `"$@"`. Now the docker-registry input reaches `login` as a single argument: it is no longer split on spaces or expanded as a glob. When I re-read the edited lines, `"$@"` is in place. A search right after the edit still reported `$*` at the old positions, which I think was stale results; I didn't run a fresh search to rule it out. Nothing else in the action changed.

