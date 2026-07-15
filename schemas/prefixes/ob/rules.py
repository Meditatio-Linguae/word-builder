from schemas.bases import Base
from schemas.prefixes import PrefixComposingRule
from schemas.prefixes.ob import Ob


class ObRightToLeftAssimilationRule(PrefixComposingRule):
    def __init__(self):
        self.rules = [
            (("c", "f", "p"), lambda p, s: p[:-1] + s[0])
        ]

    def matches(self, left, right):
        return isinstance(left, Ob) and isinstance(right, Base)

    def apply(self, left, right):
        return super().apply(left, right)
