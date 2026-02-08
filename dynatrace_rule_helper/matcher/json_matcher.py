import json
from .base import BaseMatcher

class JSONMatcher(BaseMatcher):
    """Matcher for a JSON subtree inside the log line.

    The DPL syntax is simply ``JSON:export`` – it parses a JSON string and
    exports the whole structure under the given field name.
    """

    def __init__(self, export_name: str):
        super().__init__(export_name)

    def build(self) -> str:
        return f"JSON:{self.export_name}"
