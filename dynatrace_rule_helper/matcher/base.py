"""Base class for all DPL matchers.

Each concrete matcher implements the ``build`` method that returns the DPL fragment
for that matcher, e.g. ``INT:field`` or ``TIMESTAMP('MMMMM d, yyyy HH:mm:ss'):timestamp``.
"""

from abc import ABC, abstractmethod
from typing import Optional

class BaseMatcher(ABC):
    """Abstract matcher – all concrete matchers inherit from this.

    Attributes
    ----------
    export_name: str
        The name that will be used in the ``:export`` part of the DPL fragment.
    literal: Optional[str]
        The literal text that appears before the value (may be omitted for some
        matchers like JSON or ENUM).
    value: Optional[str]
        The raw sample value – used for inference when the user does not supply
        a matcher type.
    """

    def __init__(self, export_name: str, literal: Optional[str] = None, value: Optional[str] = None):
        self.export_name = export_name
        self.literal = literal
        self.value = value

    @abstractmethod
    def build(self) -> str:
        """Return the DPL fragment for this matcher.

        Must be a string that can be placed directly inside the PARSE command.
        """
        pass

    @property
    def optional(self) -> bool:
        """Whether this matcher is optional (adds the ``?`` quantifier)."""
        return False
