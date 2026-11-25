#!/bin/bash
# Fake docker build script used by tests. Records the arguments it was called with.
set -e
{
  echo "IMAGE_NAME=$1"
  echo "FLAG=$2"
  echo "DOCKER_IMAGE=$3"
} > /tmp/build-args.txt
echo "fake build invoked with: $*"
