from schemas.latin.adjective import AdjectiveStem
from utils.composer.rule import Rule
from utils.misc import autoclone


class AdjectiveItySuffixAssimilationRule(Rule):
    def matches(self, left, right):
        return isinstance(right, AdjectiveStem) and right == "ity"
    
    def apply(self, left, right):
        cloned_left = autoclone(left)
        cloned_left.radical = autoclone(left.radical)
        cloned_right = autoclone(right)
        cloned_right.radical = autoclone(right.radical)

        if cloned_left.orth.endswith("i"):
            cloned_right.orth = "e" + cloned_right.orth[1:]
            return [(cloned_left, cloned_right)]
        # elif to_orth.endswith("r") or to_orth.endswith("t"):
        #     base.radical.orth = "ty"

        return []