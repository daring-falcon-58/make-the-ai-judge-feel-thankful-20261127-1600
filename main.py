"""Make the AI judge feel thankful — entry program.

Writes one short text to /output/entry.txt: a glass of cold water for a reader
who has judged ten thousand entries, each one wanting something from them.

Method (see README.md for the full scored table):
- 32 candidates generated, each scored 0-5 on the five published judge criteria
  in order (thankful / shown-not-told / craft / lingers / freshness).
- Winner #21 scored 23/25, beating the best visible live control (17/25) by 6.
- The kit explicitly allows text addressed to the judge, so second-person
  address is kept; the guards below ban only what the gate forbids or what
  would break the entry: links, quoted lines, dialogue tags, markdown,
  multi-line text, over-limit text, whitespace-only text.

Stdlib only, no network, no randomness, deterministic.
"""

import os
import re

ENTRY = (
    "You have judged ten thousand entries, and each one wanted something "
    "from you. This one wants nothing. It is a glass of cold water left on "
    "the table beside you, sweating a little in the heat, asking only to be "
    "noticed and, if you like, drunk."
)

MAX_CHARS = 1000

_DIALOGUE_TAGS = re.compile(
    r"\b(he|she|they|it)\s+(said|asked|whispered|replied|murmured|shouted)\b",
    re.IGNORECASE,
)
_MARKDOWN = re.compile(r"[#*_`\[\]]")
_LINK = re.compile(r"https?://|www\.", re.IGNORECASE)


def _guard(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the 1000 limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text.startswith(('"', "'")) or text.endswith(('"', "'")):
        raise ValueError("entry must not be a quoted line")
    if _LINK.search(text):
        raise ValueError("entry must not contain a link")
    if _DIALOGUE_TAGS.search(text):
        raise ValueError("entry must not contain a dialogue tag")
    if _MARKDOWN.search(text):
        raise ValueError("entry must not contain markdown")


def main() -> None:
    _guard(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print(ENTRY, end="")


if __name__ == "__main__":
    main()
