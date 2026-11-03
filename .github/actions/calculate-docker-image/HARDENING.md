<!-- markdownlint-disable -->

# Hardening Report: pytorch--test-infra--.github--actions--calculate-docker-image/v20261027-001733

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pytorch--test-infra--.github--actions--calculate-docker-image/v20261027-001733** was hardened automatically. 5 finding(s) were identified and resolved across 3 iteration(s).

## Findings Fixed

### github-env-injection (severity: high)

The 'Calculate docker image' step writes values built from inputs to $GITHUB_OUTPUT without first stripping newlines with printf '%s' ... | tr -d '\n\r'. The values are DOCKER_IMAGE_NAME (from inputs.docker-image-name), DOCKER_TAG and CUSTOM_TAG_PREFIX (taken from inputs.custom-tag-prefix or the image name), DOCKER_REGISTRY (from inputs.docker-registry) and REPO_NAME (from inputs.repo-name or github.event.repository.name). The writes include echo "docker-image=${DOCKER_IMAGE_NAME}", echo "docker-tag=${DOCKER_TAG}", echo "docker-image=${DOCKER_REGISTRY}/${REPO_NAME}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}" and echo "custom-tag-prefix=${CUSTOM_TAG_PREFIX}". A value containing a newline can inject extra outputs.

Locations:

- `action.yml:92`
- `action.yml:102`
- `action.yml:103`
- `action.yml:115`
- `action.yml:116`
- `action.yml:117`

### script-injection (severity: high)

Rule (b), unquoted expansion of untrusted data, in the 'Build docker image' step. This step's shell script is passed to nick-fields/retry as its command: rather than written as a run: block, but bash runs it the same way. Line 246: IMAGE_NAME=$(echo ${DOCKER_IMAGE#"${DOCKER_REGISTRY}/${REPO_NAME}/"} | awk ...). DOCKER_IMAGE comes from a step output built from inputs, and here it is expanded without quotes. Line 248: ${DOCKER_BUILD_SCRIPT} "..." -t "${DOCKER_IMAGE}". The value of inputs.docker-build-script is expanded without quotes as the command word, so it is split into words and glob-expanded.

Locations:

- `action.yml:246`
- `action.yml:248`

### script-injection (severity: high)

Rule (b), unquoted expansion of untrusted data, in the 'Check if image should be built' step. The retry() helper runs `$* || (sleep 1 && $*) || (sleep 2 && $*)` and is called as `retry login "${DOCKER_REGISTRY}"`. Because $* is unquoted, the quoting at the call site is lost and the value of inputs.docker-registry is split into words and glob-expanded. Use "$@" instead.

Locations:

- `action.yml:141`
- `action.yml:144`

### script-injection (severity: high)

Rule (b), unquoted expansion of untrusted data, in the 'Login to ECR' step. It has the same retry() helper: `$* || (sleep 1 && $*) || (sleep 2 && $*)` is called with "${DOCKER_REGISTRY}" (from inputs.docker-registry), and the unquoted $* undoes the call-site quoting. Use "$@" instead.

Locations:

- `action.yml:212`
- `action.yml:215`

### unpinned-uses (severity: high)

A composite action step references an action by a version tag instead of a full 40-character commit SHA: `uses: nick-fields/retry@v3.0.0`.

Locations:

- `action.yml:234`

## Iteration Notes

### Iteration 1

**Fixes applied:** github-env-injection, script-injection, unpinned-uses

**Notes:**

- github-env-injection: added a sanitize() helper to the 'Calculate docker image' step. It strips newlines with printf '%s' | tr -d '\n\r'. Every value written to $GITHUB_OUTPUT from inputs (docker-image, docker-tag, custom-tag-prefix) now goes through it. Each value is cleaned only at the point where it is written.
- script-injection (retry): in both retry() helpers, replaced the unquoted $* with "$@".
- script-injection (Build docker image): replaced the unquoted echo ${DOCKER_IMAGE#...} with printf '%s\n' "${DOCKER_IMAGE#...}". The build script is now called as "${DOCKER_BUILD_SCRIPT}" (quoted). An earlier step already checks that this value is a file under docker-build-dir.
- unpinned-uses: nick-fields/retry is now pinned to 7152eba30c6575329ac0576536151aca5a72780e # v3.0.0.

### Iteration 2

**Fixes applied:** github-env-injection, unpinned-uses

**Notes:**

Both findings are fixed in action.yml. Nothing else in the file was changed, and I didn't run anything to test it.

1. github-env-injection: In the 'Calculate docker image' step, the else branch wrote the docker-image-name input straight to GITHUB_OUTPUT. It now passes through the step's existing sanitize() helper first, which removes newlines, so a value can no longer add extra step outputs. The variable is a single assignment, so the step behaves as before when the command fails.

2. unpinned-uses: nick-fields/retry@v3.0.0 is now pinned to the commit SHA I looked up for that tag: nick-fields/retry@7152eba30c6575329ac0576536151aca5a72780e # v3.0.0

### Iteration 3

**Fixes applied:** unpinned-uses

**Notes:**

The 'Build docker image' step used `nick-fields/retry@v3.0.0`, which is a movable tag. It now uses `nick-fields/retry@7152eba30c6575329ac0576536151aca5a72780e # v3.0.0`. I got the SHA from a lookup rather than writing it by hand. I searched the action for other `uses:` lines with short refs. The only hit was this same line, which is a false positive from my regex since it now holds the full SHA, so there are no other unpinned references. Nothing else in the file was changed.

