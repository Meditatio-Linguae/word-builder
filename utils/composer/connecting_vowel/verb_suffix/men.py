from schemas.latin.verb import VerbStem
from utils.composer.connecting_vowel import ConnectingVowel
from utils.composer.rule import Rule


class VerbWithMenSuffixConnectingVowelRule(Rule):
    def matches(self, left, right):
        return right.orth == "men" and isinstance(left, VerbStem)
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]