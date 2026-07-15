from schemas.bases import Base
from schemas.prefixes import PrefixComposingRule
from schemas.prefixes.in_ import In


class InRightToLeftAssimilationRule(PrefixComposingRule):
    def __init__(self):
        self.rules = [
            (("b", "m", "p"), lambda p, s: p[:-1] + "m"),
            (("l", "r"), lambda p, s: p[:-1] + s[0])
        ]

    def matches(self, left, right):
        return isinstance(left, In) and isinstance(right, Base)

    def apply(self, left, right):
        return super().apply(left, right)
