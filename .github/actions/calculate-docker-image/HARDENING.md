<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261119-192116

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261119-192116** was hardened automatically. 3 finding(s) were identified and resolved across 3 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

Step 'Calculate docker image' writes values taken from workflow inputs to $GITHUB_OUTPUT without first stripping newlines with printf '%s' ... | tr -d '\n\r'. The inputs are DOCKER_IMAGE_NAME (inputs.docker-image-name), DOCKER_REGISTRY, REPO_NAME (inputs.repo-name or github.event.repository.name) and CUSTOM_TAG_PREFIX (inputs.custom-tag-prefix), plus DOCKER_TAG, which is built from them. The writes are: echo "docker-image=${DOCKER_IMAGE_NAME}", echo "docker-tag=${DOCKER_TAG}", echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" and echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}". A value containing a newline can add extra step outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### unpinned-uses (severity: high)

The composite step 'Build docker image' uses an action by a version tag, not a full 40-character commit SHA: 'uses: nick-fields/retry@v3.0.0'.

Locations:

- `action.yml:234`

### script-injection (severity: high)

Rule (b), unquoted expansion. The shell script in the 'Build docker image' step (passed to nick-fields/retry as `command:` and run by bash) expands workflow-controlled data without quotes: `IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...)`. DOCKER_IMAGE comes from steps.calculate-image.outputs.docker-image, which is built from inputs. It should be double-quoted: "${DOCKER_IMAGE#...}".

Locations:

- `action.yml:246`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, unpinned-uses, script-injection

**Notes:**

All changes are in action.yml.

- github-env-injection: the 'Calculate docker image' step now strips newlines from DOCKER_IMAGE_NAME, DOCKER_REGISTRY, REPO_NAME and CUSTOM_TAG_PREFIX right at the start with printf '%s' | tr -d '\n\r'. Every write to $GITHUB_OUTPUT (docker-image, docker-tag, custom-tag-prefix) also uses a separately stripped value. Each stripped value is captured in its own assignment, so errexit still behaves as before. DOCKER_TAG is stripped too, since it is built from these inputs.
- unpinned-uses: nick-fields/retry is pinned to 7152eba30c6575329ac0576536151aca5a72780e (# v3.0.0). I got the SHA from lookup_action_sha.
- script-injection: in the retry command, the ${DOCKER_IMAGE#...} expansion passed to echo is now double-quoted. It is a single value, so quoting it does not change behavior.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Replaced unquoted $* with "$@" in both retry helpers (the 'Check if image should be built' and 'Login to ECR' steps), so the DOCKER_REGISTRY argument stays a single quoted word.

### Iteration 3

**Fixes applied:** script-injection

**Notes:**

Quoted ${DOCKER_BUILD_SCRIPT} in the 'Build docker image' step's nick-fields/retry command. The input is documented as a single script path (default ./build.sh, relative to the docker-build-dir), so quoting keeps how it behaves for a normal path. It also means the shell no longer splits or glob-expands the value.

