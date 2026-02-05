#!/usr/bin/env python3
"""
Dynatrace Rule Helper – refined version
--------------------------------------

This tool generates a **Dynatrace PARSE rule** (DPL) based on a sample log line
and explicit extraction instructions supplied by the user.

Key concepts
~~~~~~~~~~~~
* **LD** – *Line Data* matcher that extracts a token after a literal.
* **SPACE?** – optional whitespace after the literal (as shown in the docs).
* **Matcher** – the data‑type of the extracted token (INT, FLOAT, STRING, …).
* **Export name** – the field name you want to appear in Dynatrace
  (e.g. ``aws.billed.duration``).

Typical usage (single field)::

    python dynatrace_rule_helper.py \
        -f sample3.json \
        -l "Billed Duration:" \
        -v 5034 \
        -t INT \
        -a aws.billed.duration

Result::

    PARSE(content, "LD 'Billed Duration:' SPACE? INT:aws.billed.duration")

Multiple extractions can be specified by separating the arguments with commas:

    -l "Billed Duration:,Duration:" -a "aws.billed.duration,aws.duration" -t "INT,FLOAT"

The script also supports a heuristic mode – if you omit `-l`/`-v`/`-t`, it will try to infer the literal and matcher from the sample log.
"""

import argparse
import json
import re
import sys
from typing import List, Tuple

# ---------------------------------------------------------------------
# Helper functions – matcher inference & pattern building
# ---------------------------------------------------------------------

def infer_matcher_from_value(value: str) -> str:
    """Return a DPL matcher name based on the supplied string value.
    INT   – integer numbers (no decimal point)
    FLOAT – numbers with a decimal point
    STRING – everything else
    """
    if re.fullmatch(r"-?\d+", value):
        return "INT"
    if re.fullmatch(r"-?\d+\.\d+", value):
        return "FLOAT"
    return "STRING"

def escape_literal(lit: str) -> str:
    """Escape single quotes for DPL literal syntax."""
    return lit.replace("'", "\\'")

def build_single_fragment(literal: str, matcher: str, alias: str) -> str:
    """Create the DPL snippet for ONE extraction.
    Example -> "LD 'Billed Duration:' SPACE? INT:aws.billed.duration"
    """
    escaped = escape_literal(literal)
    return f"LD '{escaped}' SPACE? {matcher}:{alias}"

def parse_content_for_value(content: str, value: str) -> Tuple[str, str]:
    """Find the literal that directly precedes the *value* in *content*.
    Returns (literal, value). If not found, returns ("", value).
    The function looks backwards from the value start until it meets a non‑
    whitespace character that is not a digit or decimal point, then captures
    the preceding characters as the literal.
    """
    idx = content.find(value)
    if idx == -1:
        return "", value
    # Scan backwards to find the start of the preceding literal (skip spaces)
    pre_end = idx
    while pre_end > 0 and content[pre_end - 1].isspace():
        pre_end -= 1
    # Now go further back until we hit a character that could be part of the literal
    pre_start = pre_end
    while pre_start > 0 and not content[pre_start - 1].isspace():
        pre_start -= 1
    literal = content[pre_start:pre_end]
    return literal, value

# ---------------------------------------------------------------------
# Core builder – supports both explicit literals and heuristic fallback
# ---------------------------------------------------------------------

def build_dpl_rule(literals: List[str], matchers: List[str], aliases: List[str]) -> str:
    """Combine one or more extraction fragments into a full PARSE rule.
    The three lists must be of equal length; each position corresponds to a single
    extraction.
    """
    fragments = []
    for lit, m, alias in zip(literals, matchers, aliases):
        fragments.append(build_single_fragment(lit, m, alias))
    inner = " ".join(fragments)
    return f'PARSE(content, "{inner}")'

# ---------------------------------------------------------------------
# CLI handling
# ---------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Generate Dynatrace PARSE rules (DPL) from a sample log line.")
    p.add_argument("-f", "--file", required=True,
                   help="Path to JSON file containing the raw log record (must have a 'content' field).")
    p.add_argument("-l", "--literal",
                   help="Comma‑separated literal(s) that precede the value(s) to extract. Optional – if omitted, inferred.")
    p.add_argument("-v", "--value",
                   help="Comma‑separated value(s) to extract (used for literal inference). Optional.")
    p.add_argument("-t", "--type",
                   help="Comma‑separated matcher type(s) (INT, FLOAT, STRING). Optional – inferred from value if omitted.")
    p.add_argument("-a", "--alias", required=True,
                   help="Comma‑separated field name(s) for the extracted data (e.g., 'aws.billed.duration').")
    return p.parse_args()

# ---------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------

def main():
    args = parse_args()

    # Load JSON file
    try:
        with open(args.file, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    content = data.get("content")
    if not content:
        print("JSON must contain a 'content' field with the raw log line.", file=sys.stderr)
        sys.exit(1)

    # Split comma‑separated arguments
    aliases = [a.strip() for a in args.alias.split(",") if a.strip()]
    literals_input = [l.strip() for l in args.literal.split(",")] if args.literal else []
    values_input = [v.strip() for v in args.value.split(",")] if args.value else []
    types_input = [t.strip().upper() for t in args.type.split(",")] if args.type else []

    n = len(aliases)
    if literals_input and len(literals_input) != n:
        print("Number of literals must match number of aliases.", file=sys.stderr)
        sys.exit(1)
    if values_input and len(values_input) != n:
        print("Number of values must match number of aliases.", file=sys.stderr)
        sys.exit(1)
    if types_input and len(types_input) != n:
        print("Number of types must match number of aliases.", file=sys.stderr)
        sys.exit(1)

    # Resolve literals – use supplied or infer from values (or fallback to empty string)
    literals = []
    for i in range(n):
        if literals_input:
            literals.append(literals_input[i])
        elif values_input:
            lit, _ = parse_content_for_value(content, values_input[i])
            literals.append(lit)
        else:
            literals.append("")

    # Resolve matchers – use supplied or infer from values (or default to STRING)
    matchers = []
    for i in range(n):
        if types_input:
            matchers.append(types_input[i])
        elif values_input:
            matchers.append(infer_matcher_from_value(values_input[i]))
        else:
            matchers.append("STRING")

    # Build the DPL rule
    dpl_rule = build_dpl_rule(literals, matchers, aliases)
    print("--- Suggested Dynatrace PARSE rule ---")
    print(dpl_rule)
    print("--- End of rule ---")

if __name__ == "__main__":
    main()
