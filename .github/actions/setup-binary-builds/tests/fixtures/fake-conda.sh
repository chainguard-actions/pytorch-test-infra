#!/usr/bin/env bash
# Fake conda used by tests: records every invocation to /tmp/fake-conda.log
# and emulates just enough behaviour for the setup-binary-builds action.
LOG="/tmp/fake-conda.log"
echo "conda $*" >> "$LOG"
case "$1" in
  info)
    echo "     active environment : None"
    echo "       base environment : /opt/fake-conda  (writable)"
    ;;
  --version)
    echo "conda 24.7.1"
    ;;
  clean|config|install|uninstall|list)
    ;;
  create)
    prefix=""
    prev=""
    for a in "$@"; do
      if [ "$prev" = "--prefix" ] || [ "$prev" = "-p" ]; then prefix="$a"; fi
      prev="$a"
    done
    if [ -n "$prefix" ]; then mkdir -p "$prefix"; fi
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
    if [ "$1" = "python" ] && [ "$2" = "-m" ] && [ "$3" = "pip" ]; then
      echo "fake pip: $*"
      exit 0
    fi
    if [ "$1" = "python" ] && [ "$2" = "-m" ] && [ "$3" = "pytorch_pkg_helpers" ]; then
      echo "export FAKE_PKG_HELPER=1"
      echo "export BUILD_VERSION=0.0.0.dev"
      exit 0
    fi
    exec "$@"
    ;;
  *)
    ;;
esac
exit 0
