from utils.composer.connecting_vowel import ConnectingVowel
from schemas.latin.noun import NounClassNo, NounStem
from utils.composer.rule import Rule


class NounWithCleSuffixConnectingVowelRule(Rule):
    def matches(self, left, right):
        return right.orth == "cle" and (right.declension_required in [NounClassNo.III, NounClassNo.IV, NounClassNo.V] and (isinstance(left, NounStem) and left.declension_no in [NounClassNo.III, NounClassNo.IV, NounClassNo.V]))
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]
