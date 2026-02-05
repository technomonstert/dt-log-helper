import re
from typing import Optional

from .base import BaseMatcher

class TimestampMatcher(BaseMatcher):
    """Matcher for timestamps using the DPL ``TIMESTAMP`` function.

    The constructor receives a ``pattern`` string that follows the DPL syntax,
    e.g. ``'MMMMM d, yyyy HH:mm:ss'``.
    """

    def __init__(self, export_name: str, pattern: str, literal: Optional[str] = None):
        super().__init__(export_name, literal)
        self.pattern = pattern

    def build(self) -> str:
        # Build the DPL fragment – if a literal is present we prepend it as LD
        if self.literal:
            # Escape any single quotes inside the literal
            escaped = self.literal.replace("'", "\\'")
            return f"LD '{escaped}' SPACE? TIMESTAMP('{self.pattern}'):{self.export_name}"
        return f"TIMESTAMP('{self.pattern}'):{self.export_name}"

    @staticmethod
    def infer_pattern(sample: str) -> Optional[str]:
        """Infer a DPL timestamp pattern from a sample timestamp string.
        Supports the common ``April 24, 2022 09:59:52`` format used in the docs.
        Returns the DPL pattern string or ``None`` if not matched.
        """
        # Simple regex for the example format – can be extended later
        m = re.search(r"(?P<month>[A-Za-z]+)\s+(?P<day>\d{1,2}),\s+(?P<year>\d{4})\s+(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})", sample)
        if not m:
            return None
        # Replace captured groups with DPL tokens
        pattern = "MMMMM d, yyyy HH:mm:ss"
        return pattern
