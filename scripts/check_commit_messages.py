import re
import subprocess
import sys

COMMIT_PATTERN = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(\([a-zA-Z0-9._/-]+\))?!?: .{1,72}$"
)


def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/check_commit_messages.py <base-sha> <head-sha>")
        return 2

    base_sha, head_sha = sys.argv[1:3]

    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--format=%s",
                f"{base_sha}..{head_sha}",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        print("ERROR: Unable to read pull request commit messages.")
        return 2

    messages = result.stdout.splitlines()

    if not messages:
        print("No commits found to validate.")
        return 0

    invalid_messages = [
        message for message in messages if not COMMIT_PATTERN.fullmatch(message)
    ]

    if invalid_messages:
        print("Commit message validation failed.")

        for message in invalid_messages:
            print(f"  Invalid: {message}")

        print("\nExpected format: type(optional-scope): description")

        return 1

    print("Commit message validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
