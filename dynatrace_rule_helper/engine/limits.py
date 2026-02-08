"""Enforce Dynatrace‑specific limits on rule size, fragment count, etc.
"""

MAX_RULE_SIZE = 10_000          # bytes (≈ 10 KB)
MAX_LITERAL_SIZE = 256_000        # per literal/value
MAX_FRAGMENTS = 50               # practical UI limit

class RuleSizeExceededError(Exception):
    pass

def enforce_rule_size(rule_str: str) -> None:
    if len(rule_str.encode("utf-8")) > MAX_RULE_SIZE:
        raise RuleSizeExceededError(f"Rule exceeds max size of {MAX_RULE_SIZE} bytes.")

def validate_literal(literal: str) -> None:
    if len(literal.encode("utf-8")) > MAX_LITERAL_SIZE:
        raise RuleSizeExceededError(f"Literal/value exceeds max size of {MAX_LITERAL_SIZE} bytes.")

def validate_fragment_count(fragments: list) -> None:
    if len(fragments) > MAX_FRAGMENTS:
        raise RuleSizeExceededError(f"Number of fragments ({len(fragments)}) exceeds limit of {MAX_FRAGMENTS}.")
