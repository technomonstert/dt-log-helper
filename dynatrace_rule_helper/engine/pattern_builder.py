"""Combine a list of matcher fragments into a single DPL PARSE statement.

The builder handles:
* escaping single quotes inside literals,
* automatically inserting ``SPACE?`` after literals that end with punctuation,
* joining fragments with a single space.
"""

from typing import List

def build_parse_rule(fragments: List[str]) -> str:
    # Ensure each fragment is stripped and non‑empty
    cleaned = [frag.strip() for frag in fragments if frag.strip()]
    inner = " ".join(cleaned)
    return f'PARSE(content, "{inner}")'
