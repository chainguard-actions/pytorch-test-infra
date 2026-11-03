#!/bin/sh
# Fake Homebrew python: logs invocations; `-m venv DIR` creates DIR/bin/python (also fake).
echo "python $*" >> "$FAKE_LOG"
if [ "$1" = "-m" ] && [ "$2" = "venv" ]; then
  mkdir -p "$3/bin"
  printf '#!/bin/sh\necho "venvpython $*" >> "$FAKE_LOG"\nexit 0\n' > "$3/bin/python"
  chmod +x "$3/bin/python"
fi
exit 0
