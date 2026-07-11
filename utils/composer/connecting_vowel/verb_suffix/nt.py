from schemas.latin.verb import (
    VerbAssimilatedRadicalStem,
    VerbClassNo,
    VerbIrregularPresentInfinitiveStem,
    VerbRegularPresentInfinitiveStem,
    VerbStem,
)
from utils.composer.rule import Rule
from utils.misc import autoclone


class VerbWithNtSuffixAssimilationRule(Rule):
    def matches(self, left, right):
        return right.orth == "nt" and isinstance(left, VerbStem)

    def apply(self, left, right):
        #TODO: magnificent but significant
        cloned_left = autoclone(left)
        cloned_left.radical = autoclone(left.radical)
        cloned_right = autoclone(right)
        cloned_right.radical = autoclone(right.radical)
        if (isinstance(cloned_left, VerbRegularPresentInfinitiveStem) and (cloned_left.conjugation_no == VerbClassNo.IV or (cloned_left.conjugation_no == VerbClassNo.III and cloned_left.is_istem))) or (isinstance(cloned_left, VerbIrregularPresentInfinitiveStem) and not cloned_left.orth.endswith("e")):
            cloned_right.orth = "e" + cloned_right.orth
        return [(cloned_left, cloned_right)]
