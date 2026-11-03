#!/usr/bin/env bash
# Fake conda used by the tests: logs every invocation and emulates the
# subcommands used by the setup-binary-builds action.
LOG="${FAKE_CONDA_LOG:-/tmp/fake-conda.log}"
echo "conda $*" >> "$LOG"
case "$1" in
  info)
    echo "     active environment : None"
    echo "       base environment : /opt/fake-conda  (writable)"
    ;;
  --version)
    echo "conda 24.7.1"
    ;;
  create)
    prev=""
    for a in "$@"; do
      if [ "$prev" = "--prefix" ] || [ "$prev" = "-p" ]; then
        mkdir -p "$a"
      fi
      prev="$a"
    done
    ;;
  run)
    if [[ "$*" == *"-m pytorch_pkg_helpers"* ]]; then
      echo "export FAKE_PKG_HELPER=1"
      echo "export BUILD_VERSION=0.0.0"
    fi
    ;;
esac
exit 0
