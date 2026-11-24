#!/bin/bash
# Fake conda used by the tests: records every invocation and simulates the
# subcommands the action uses, so no real conda/network install is needed.
LOG="${FAKE_CONDA_LOG:-/tmp/fake-conda.log}"
echo "conda $*" >> "$LOG"
case "$1" in
  info)
    echo "     active environment : None"
    echo "       base environment : /opt/fakeconda  (writable)"
    ;;
  --version)
    echo "conda 24.7.1"
    ;;
  create)
    prev=""
    for arg in "$@"; do
      if [ "$prev" = "--prefix" ]; then
        mkdir -p "$arg"
      fi
      prev="$arg"
    done
    ;;
  run)
    shift
    while [ $# -gt 0 ]; do
      case "$1" in
        --no-capture-output) shift ;;
        -p|--prefix) shift 2 ;;
        *) break ;;
      esac
    done
    if [ "$1" = "python" ] && [ "$2" = "-m" ] && [ "$3" = "pytorch_pkg_helpers" ]; then
      echo "export FAKE_PKG_HELPERS=generated"
    fi
    ;;
esac
exit 0
