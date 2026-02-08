"""Utility functions for extracting literals, inferring matchers, etc.
"""

import re
from typing import List, Tuple, Optional

def infer_literal_from_value(content: str, value: str) -> Tuple[str, str]:
    """Return the literal that directly precedes *value* in *content*.

    The function scans *content* for the first occurrence of *value* and then
    walks backwards until it hits a whitespace character.  The slice between the
    whitespace and the start of *value* is considered the literal.
    """
    idx = content.find(value)
    if idx == -1:
        return "", value
    # Walk backwards over spaces
    pre_end = idx
    while pre_end > 0 and content[pre_end - 1].isspace():
        pre_end -= 1
    # Walk further back until another whitespace (or start of line)
    pre_start = pre_end
    while pre_start > 0 and not content[pre_start - 1].isspace():
        pre_start -= 1
    literal = content[pre_start:pre_end]
    return literal, value

def guess_matcher_type(value: str) -> str:
    """Very naive type inference – returns one of the DPL matcher names.

    * integer → ``INT``
    * float   → ``FLOAT``
    * looks like an IP → ``IPADDR``
    * looks like a URL → ``URL``
    * otherwise ``STRING``
    """
    if re.fullmatch(r"-?\d+", value):
        return "INT"
    if re.fullmatch(r"-?\d+\.\d+", value):
        return "FLOAT"
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", value):
        return "IPADDR"
    if re.match(r"^https?://", value):
        return "URL"
    return "STRING"
