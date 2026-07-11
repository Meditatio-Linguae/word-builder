from schemas.latin.adjective import AdjectiveStem
from schemas.latin.adverb import AdverbStem
from schemas.latin.noun import NounStem
from schemas.latin.preposition import Preposition
from schemas.latin.verb import (
    VerbAssimilatedRadicalStem, 
    VerbRegularPerfectParticipleStem, 
    VerbRegularPresentInfinitiveStem
)
from utils.composer.rule import Rule
from utils.misc import autoclone


class VerbAssimilationRule(Rule):
    def matches(self, left, right):
        return (
            isinstance(right, (VerbAssimilatedRadicalStem, VerbRegularPresentInfinitiveStem, VerbRegularPerfectParticipleStem))
            and isinstance(left, (Preposition, NounStem, AdverbStem, AdjectiveStem))
            and right.orth in self._REPLACEMENTS
        )

    def apply(self, left, right):
        cloned_left = autoclone(left)
        cloned_left.radical = autoclone(left.radical)
        cloned_right = autoclone(right)
        cloned_right.radical = autoclone(right.radical)
        cloned_right.orth = self._REPLACEMENTS[cloned_right.orth]
        return [(cloned_left, cloned_right)]


class VerbAssimilatedRadicalStemAssimilationRule(VerbAssimilationRule):
    _REPLACEMENTS = {
        "cad": "cid",
        "cap": "cip",
        "fac": "fic",
        "hab": "hib",
        "jac": "jic",
        "salt": "sult",
        "scand": "scend",
        "spec": "spic",
        "sed": "sid",
    }
    

class VerbRegularPresentInfinitiveStemAssimilationRule(VerbAssimilationRule):
    _REPLACEMENTS = {
        "cade": "cide",
        "cape": "cipe",
        "faci": "fici",
        "habe": "hibe",
        "jaci": "jici",
        "scande": "scende",
        "speci": "speci",
        "sede": "side"
    }


class VerbRegularPerfectParticipleStemAssimilationRule(VerbAssimilationRule):
    _REPLACEMENTS = {
        "cas": "cis",
        "capt": "cept",
        "fact": "fect",
        "habit": "hibit",
        "jact": "ject",
        "scans": "scens"
    }