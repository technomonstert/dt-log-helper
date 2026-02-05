from .base import BaseMatcher

class StringMatcher(BaseMatcher):
    def __init__(self, export_name: str, literal: str = None):
        super().__init__(export_name, literal)

    def build(self) -> str:
        if self.literal:
            escaped = self.literal.replace("'", "\\'")
            return f"LD '{escaped}' SPACE? STRING:{self.export_name}"
        return f"STRING:{self.export_name}"
