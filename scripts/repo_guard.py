import subprocess
import sys
from pathlib import Path

FORBIDDEN_NAMES = {
    ".env",
}

FORBIDDEN_SUFFIXES = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".pyc",
    ".so",
    ".dll",
    ".exe",
}


def get_tracked_files():
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )

    return [Path(name.decode("utf-8")) for name in result.stdout.split(b"\0") if name]


def is_forbidden(path):
    name = path.name.lower()

    if name in FORBIDDEN_NAMES:
        return True

    if name.startswith(".env."):
        return name != ".env.example"

    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        return True

    return False


def main():
    try:
        tracked_files = get_tracked_files()
    except subprocess.CalledProcessError:
        print("ERROR: Unable to inspect tracked Git files.")
        return 2

    forbidden_files = [path for path in tracked_files if is_forbidden(path)]

    if forbidden_files:
        print("Repository guard failed.")
        print("The following tracked files are prohibited:")

        for path in forbidden_files:
            print(f"  - {path}")

        return 1

    print("Repository guard passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
