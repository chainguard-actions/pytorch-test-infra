import os

for key in ("REPOSITORY", "REF", "PYTHON_VERSION", "CU_VERSION", "ARCH"):
    print(f"export FAKE_{key}={os.environ.get(key, '')}")
print(f"export FAKE_CWD={os.getcwd()}")
