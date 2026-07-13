from schemas.bases import Base
from schemas.prefixes import PrefixComposingRule
from schemas.prefixes.ad import Ad


class AdRightToLeftAssimilationRule(PrefixComposingRule):
    def __init__(self):
        self.rules = [
            (("c", "f", "g", "l", "n", "p", "r", "s", "t"), lambda p, s: p[:-1] + s[0]),
            (("q"), lambda p, s: p[:-1] + "c"),
            (("t"), lambda p, s: p[:-1] + "s"),
            (("m"), lambda p, s: p[:-1]),
        ]

    def matches(self, left, right):
        return isinstance(left, Ad) and isinstance(right, Base)

    def apply(self, left, right):
        return super().apply(left, right)
