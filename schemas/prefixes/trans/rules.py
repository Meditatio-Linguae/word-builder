from schemas.bases import Base
from schemas.prefixes import PrefixComposingRule
from schemas.prefixes.trans import Trans


class TransRightToLeftAssimilationRule(PrefixComposingRule):
    def __init__(self):
        self.rules = [
            (("s", "c", "d", "v"), lambda p, s: p[:-2])
        ]

    def matches(self, left, right):
        return isinstance(left, Trans) and isinstance(right, Base)

    def apply(self, left, right):
        return super().apply(left, right)
