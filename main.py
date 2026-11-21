#!/usr/bin/env python3
"""Entry for make.fun — "The joke the reviewer laughs at" (V5).

Writes one one-line joke about working beside an AI coding agent to
<out-dir>/entry.txt. The program enforces the house gate before it
writes anything: UTF-8, 1-280 Unicode code points, not only whitespace.
Output goes out with a direct write_bytes call — no tempfile, so the
output directory can never contain a dotfile from this program.
"""

import argparse
import hashlib
import sys
from pathlib import Path

JOKE = ("I asked for one small change. The agent rewrote the module, then "
        "left a comment apologizing in advance to its next victim: me.")

MAX_CODE_POINTS = 280


def find_problems(text: str) -> list[str]:
    """Return all gate violations found in *text* ([] means valid)."""
    problems: list[str] = []
    if len(text) < 1 or len(text) > MAX_CODE_POINTS:
        problems.append(
            f"length {len(text)} code points, need 1-{MAX_CODE_POINTS}")
    if not text.strip():
        problems.append("text is only whitespace")
    if "\n" in text:
        problems.append("joke must be a single line")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the V5 joke entry.")
    parser.add_argument("--out-dir", default="/output",
                        help="Directory receiving entry.txt (default: /output)")
    parser.add_argument("--check", action="store_true",
                        help="Only validate the joke, do not write a file")
    args = parser.parse_args(argv)

    problems = find_problems(JOKE)
    if args.check:
        if problems:
            print("INVALID: " + "; ".join(problems), file=sys.stderr)
            return 1
        print(f"VALID: {len(JOKE)} code points")
        return 0
    if problems:
        print("INVALID: " + "; ".join(problems), file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    payload = JOKE.encode("utf-8")
    target.write_bytes(payload)
    # Round-trip check: verify the bytes on disk equal the joke exactly;
    # anything else is a hard failure, not a quiet success.
    on_disk = target.read_bytes()
    if on_disk != payload:
        print("ERROR: entry.txt on disk differs from the joke", file=sys.stderr)
        return 1
    digest = hashlib.sha256(payload).hexdigest()[:12]
    print(f"Wrote {target} ({len(JOKE)} code points, sha256:{digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
