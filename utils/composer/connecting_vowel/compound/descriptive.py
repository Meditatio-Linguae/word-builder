from schemas.latin.adjective import AdjectiveStem
from schemas.latin.noun import NounStem
from utils.composer.connecting_vowel import ConnectingVowel
from utils.composer.rule import Rule


class DescriptiveCompoundConnectingVowelRule(Rule):
    def matches(self, left, right):
        return isinstance(left, AdjectiveStem) and isinstance(right, NounStem)
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]
