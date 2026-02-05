from .base import BaseMatcher

class URLMatcher(BaseMatcher):
    def __init__(self, export_name: str, literal: str = None):
        super().__init__(export_name, literal)

    def build(self) -> str:
        if self.literal:
            escaped = self.literal.replace("'", "\\'")
            return f"LD '{escaped}' SPACE? URL:{self.export_name}"
        return f"URL:{self.export_name}"
