from schemas.latin.verb import VerbStem
from utils.composer.connecting_vowel import ConnectingVowel
from utils.composer.rule import Rule


class VerbWithMentSuffixConnectingVowelRule(Rule):
    def matches(self, left, right):
        return right.orth == "ment" and isinstance(left, VerbStem)
    
    def apply(self, left, right):
        return [
            (left, ConnectingVowel(orth="u"), right),
            (left, ConnectingVowel(orth="o"), right),
            (left, ConnectingVowel(orth="a"), right)
        ]