from schemas.latin.adjective import AdjectiveSuffix
from schemas.latin.noun import NounStem, NounSuffix
from utils.composer.rule import Rule
from utils.misc import autoclone


class UleAdjectiveFormingSuffixAssimilationRule(Rule):
    def matches(self, left, right):
        return right.orth == "ule" and isinstance(left, NounStem) and isinstance(right, NounSuffix)
    
    def apply(self, left, right):
        cloned_left = autoclone(left)
        cloned_left.radical = autoclone(left.radical)
        cloned_right = autoclone(right)
        cloned_right.radical = autoclone(right.radical)

        if cloned_left.orth.endswith(("e", "i", "u")):
            cloned_right.orth = "o" + cloned_right.orth[1:]
            return [(cloned_left, cloned_right)]
        
        return []
    

class UleSuffixCombinationAssimilationRule(Rule):
    def matches(self, left, right):
        return left.orth == "ule" and isinstance(right, AdjectiveSuffix)
    
    def apply(self, left, right):
        cloned_left = autoclone(left)
        cloned_left.radical = autoclone(left.radical)
        cloned_right = autoclone(right)
        cloned_right.radical = autoclone(right.radical)
        cloned_left.orth = cloned_left.orth[:-1]
        return [(cloned_left, cloned_right)]
