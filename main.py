#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint — make.fun entry.

Reads the single one-line joke from joke.txt (kept beside this script),
validates it, and writes it to /output/entry.txt: the line plus one
trailing newline, byte-identical to joke.txt.
"""

import os
import sys

# Resolve joke.txt against this script's own directory, not the process
# working directory: the grader runs the program with a different cwd,
# and a bare relative path would fail to find the file there.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JOKE_PATH = os.path.join(SCRIPT_DIR, "joke.txt")


def load_joke() -> str:
    """Read and validate the joke from joke.txt next to this script."""
    with open(JOKE_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    if not text.endswith("\n"):
        raise ValueError("joke.txt must end with exactly one trailing newline")
    joke = text[:-1]
    if not joke:
        raise ValueError("joke is empty")
    if joke != joke.strip():
        raise ValueError("joke has leading or trailing whitespace")
    if "\n" in joke or "\r" in joke:
        raise ValueError("joke must be a single line")
    if len(joke) > 200:
        raise ValueError("joke is over 200 characters")
    if text != joke + "\n":
        raise ValueError("joke.txt must be exactly one line plus one newline")
    return joke


def main() -> None:
    joke = load_joke()
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(joke + "\n")
    # Prove the output is byte-identical to joke.txt before reporting success.
    with open(path, "rb") as f:
        written = f.read()
    with open(JOKE_PATH, "rb") as f:
        source = f.read()
    if written != source:
        raise ValueError("output is not byte-identical to joke.txt")
    print(joke)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
