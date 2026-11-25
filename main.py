#!/usr/bin/env python3
"""One Line, One Laugh: write a single funny line to /output/entry.txt.

The line:

    I finally found my purpose in life: it was in the pocket of the
    jeans I threw out yesterday.

Why it works as a one-liner: the first half sounds like the start of
an inspirational speech, and the second half drops it into the most
ordinary place possible -- a pocket of jeans already in the bin. The
laugh is the gap between "my purpose in life" and "yesterday's jeans",
and the whole joke is inside the sentence, so it needs no setup, no
picture and no explanation. One sentence, 92 characters, plain words
anyone can repeat to someone else.

The program keeps the line as one constant, checks it against the
competition gate (UTF-8 text, 1 to 200 characters, a single line, not
blank), then writes it with one trailing newline. It writes to the
directory the grader provides through MAKEFUN_OUTPUT_DIR, falling back
to /output and then to a local output/ folder, so the same file also
runs on a developer machine. Standard library only, no input, no
network, no clock, no randomness: every run writes the same bytes.
"""

import os
import sys

LINE = (
    "I finally found my purpose in life: it was in the pocket "
    "of the jeans I threw out yesterday."
)

MAX_CHARS = 200


def check_line(line):
    """Reject anything the gate would reject, before writing."""
    if not line or not line.strip():
        raise ValueError("line must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError("line is %d chars, over the %d cap" % (len(line), MAX_CHARS))
    return line


def pick_targets():
    """Candidate entry.txt paths, in the order to try them."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return [os.path.join(base, "entry.txt"),
            os.path.join("output", "entry.txt")]


def write_entry(payload):
    """Write the payload to the first writable target, verify it."""
    last_error = None
    for target in pick_targets():
        try:
            parent = os.path.dirname(target)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(target, "wb") as handle:
                handle.write(payload)
            with open(target, "rb") as handle:
                if handle.read() != payload:
                    raise RuntimeError("entry on disk does not match the line")
            return target
        except OSError as exc:
            last_error = exc
    raise RuntimeError("could not write entry.txt: %s" % last_error)


def main():
    line = check_line(LINE)
    payload = (line + "\n").encode("utf-8")
    target = write_entry(payload)
    print("Wrote %d characters to %s" % (len(line), target))
    print(line)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
