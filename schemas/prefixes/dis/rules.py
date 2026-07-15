from schemas.bases import Base
from schemas.prefixes import PrefixComposingRule
from schemas.prefixes.dis import Dis


class DisRightToLeftAssimilationRule(PrefixComposingRule):
    def __init__(self):
        self.rules = [
            (("r", "g", "l", "v", "m", "n"), lambda p, s: p[:-1]),
            (("f"), lambda p, s: p[:-1] + s[0])
        ]

    def matches(self, left, right):
        return isinstance(left, Dis) and isinstance(right, Base)

    def apply(self, left, right):
        return super().apply(left, right)
