from schemas.bases import Base
from schemas.prefixes import PrefixComposingRule
from schemas.prefixes.re import Re


class ReRightToLeftAssimilationRule(PrefixComposingRule):
    def __init__(self):
        self.rules = [
            (("a", "e", "i", "o", "u"), lambda p, s: p + "d")
        ]

    def matches(self, left, right):
        return isinstance(left, Re) and isinstance(right, Base)

    def apply(self, left, right):
        return super().apply(left, right)
