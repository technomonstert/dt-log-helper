from .base import BaseMatcher

class LDMatcher(BaseMatcher):
    """Line‑Data matcher – extracts the token that follows a literal.

    The DPL syntax is ``LD 'literal'``.  If ``literal`` ends with a punctuation
    character (e.g. ':' or ']') the rule should also include ``SPACE?`` to allow
    optional whitespace before the value.
    """

    def __init__(self, export_name: str, literal: str):
        super().__init__(export_name, literal)
        self.literal = literal

    def build(self) -> str:
        escaped = self.literal.replace("'", "\\'")
        # Detect if we need the optional SPACE? quantifier
        needs_space = self.literal[-1] in ":]"
        space_part = " SPACE?" if needs_space else ""
        return f"LD '{escaped}'{space_part}:{self.export_name}"
