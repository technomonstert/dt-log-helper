from .base import BaseMatcher

class IPAddrMatcher(BaseMatcher):
    def __init__(self, export_name: str, literal: str = None):
        super().__init__(export_name, literal)

    def build(self) -> str:
        if self.literal:
            escaped = self.literal.replace("'", "\\'")
            return f"LD '{escaped}' SPACE? IPADDR:{self.export_name}"
        return f"IPADDR:{self.export_name}"
