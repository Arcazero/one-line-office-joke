#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint — make.fun entry.

Reads the single one-line joke from joke.txt (kept beside this script),
validates it, and writes it to /output/entry.txt: the line plus one
trailing newline, byte-identical to joke.txt.
"""

import argparse
import os
import sys

# Resolve joke.txt against this script's own directory, not the process
# working directory: the grader runs the program with a different cwd,
# and a bare relative path would fail to find the file there.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JOKE_PATH = os.path.join(SCRIPT_DIR, "joke.txt")


def load_joke() -> str:
    """Read and validate the joke from joke.txt next to this script.

    The file must hold exactly one line plus one trailing newline, and
    the line must be 1-200 characters with no leading/trailing space.
    Error messages name the file and the offending value so a failed
    run says what to fix instead of just failing.
    """
    try:
        with open(JOKE_PATH, "r", encoding="utf-8", newline="") as f:
            text = f.read()
    except FileNotFoundError:
        raise ValueError(f"joke file not found: {JOKE_PATH}")
    except UnicodeDecodeError as exc:
        raise ValueError(f"joke.txt is not valid UTF-8: {exc}")
    if not text.endswith("\n"):
        raise ValueError("joke.txt must end with exactly one trailing newline")
    joke = text[:-1]
    if not joke:
        raise ValueError("joke is empty")
    if joke != joke.strip():
        raise ValueError("joke has leading or trailing whitespace")
    if "\n" in joke or "\r" in joke:
        raise ValueError(
            f"joke must be a single line, found {text.count(chr(10))} lines"
        )
    if len(joke) > 200:
        raise ValueError(
            f"joke is {len(joke)} characters, over the 200 limit"
        )
    if text != joke + "\n":
        raise ValueError("joke.txt must be exactly one line plus one newline")
    return joke


def verify_output(path: str) -> None:
    """Prove the written entry is byte-identical to joke.txt."""
    with open(path, "rb") as f:
        written = f.read()
    with open(JOKE_PATH, "rb") as f:
        source = f.read()
    if written != source:
        raise ValueError(
            f"output {path} ({len(written)} bytes) is not byte-identical "
            f"to joke.txt ({len(source)} bytes)"
        )


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Write the one-line office joke to /output/entry.txt."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate joke.txt only, without writing entry.txt",
    )
    args = parser.parse_args(argv)
    joke = load_joke()
    if args.check:
        print(f"ok: {len(joke)} characters, one line")
        return
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    # Atomic write: a crash mid-write must never leave a partial
    # entry.txt behind, so write a temp file in the same directory,
    # flush it to disk, then rename it over the destination.
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(joke + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)
    verify_output(path)
    print(joke)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
