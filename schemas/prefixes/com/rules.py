from schemas.bases import Base
from schemas.prefixes import PrefixComposingRule
from schemas.prefixes.com import Com


class ComRightToLeftAssimilationRule(PrefixComposingRule):
    def __init__(self):
        self.rules = [
            (("a", "e", "i", "o", "u", "h"), lambda p, s: p[:-1]),
            (("c", "d", "f", "g", "n", "q", "s", "t", "v"), lambda p, s: p[:-1] + "n"),
            (("l"), lambda p, s: p[:-1] + "l"),
            (("r"), lambda p, s: p[:-1] + "r")
        ]

    def matches(self, left, right):
        return isinstance(left, Com) and isinstance(right, Base)

    def apply(self, left, right):
        return super().apply(left, right)
