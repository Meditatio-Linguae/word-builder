from schemas.bases import Base
from schemas.prefixes import PrefixComposingRule
from schemas.prefixes.sub import Sub
from utils.misc import clone_runtime_object


class SubRightToLeftAssimilationRule(PrefixComposingRule):
    def __init__(self):
        self.rules = [
            (("c", "f", "g", "l", "r"), lambda p, s: p[:-1] + s[0]),
            (("t"), lambda p, s: p[:-1] + "s")
        ]

    def matches(self, left, right):
        return isinstance(left, Sub) and isinstance(right, Base)

    def apply(self, left, right):
        if right.orth.startswith(("p")):
            other_combinations = []
            for connecting_letter in ["p", "s"]:
                other_cloned_left = clone_runtime_object(left)
                other_cloned_left.orth = left.orth[:-1] + connecting_letter
                other_combinations.append((other_cloned_left, right))
            return other_combinations
        
        return super().apply(left, right)
