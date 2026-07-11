from utils.composer.connecting_vowel import ConnectingVowel
from schemas.latin.noun import NounClassNo, NounStem
from utils.composer.rule import Rule


class NounWithLentSuffixConnectingVowelRule(Rule):
    def matches(self, left, right):
        return right.orth == "lent"
    
    def apply(self, left, right):
        return [
            (left, ConnectingVowel(orth="u"), right),
            (left, ConnectingVowel(orth="o"), right)
        ]
