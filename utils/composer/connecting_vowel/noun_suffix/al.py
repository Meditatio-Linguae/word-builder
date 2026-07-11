from schemas.latin.noun import NounClassNo, NounStem

from utils.composer.connecting_vowel import ConnectingVowel
from utils.composer.rule import Rule


class NounWithAlSuffixConnectingVowelRule(Rule):
    def matches(self, left, right):
        return right.orth == "al" and (isinstance(left, NounStem) and left.declension_no == NounClassNo.III)
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]
