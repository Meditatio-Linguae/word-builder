from schemas.latin.adjective import AdjectiveStem
from schemas.latin.noun import NounStem
from schemas.latin.verb import VerbStem
from utils.composer.rule import Rule
from utils.misc import autoclone


class DropFirstLetterAssimilationRule(Rule):
    def matches(self, left, right):
        return isinstance(right, (NounStem, AdjectiveStem, VerbStem))
    
    def apply(self, left, right):
        cloned_left = autoclone(left)
        cloned_left.radical = autoclone(left.radical)
        cloned_right = autoclone(right)
        cloned_right.radical = autoclone(right.radical)

        if cloned_left.orth.endswith("x") and cloned_right.orth.startswith("s"):
            cloned_right.orth = cloned_right.orth[1:]
            return [(cloned_left, cloned_right)]
        #     if to_orth in ["e"]:
        #         if orth.endswith("ti"):
        #             base.radical.orth = orth[:len(orth) - 2] + "c"
        #     if to_orth in ["y"]:
        #         if orth.endswith("i"):
        #             base.radical.orth = orth[:len(orth) - 1]
            
        #     return [base] + other_bases

        return []