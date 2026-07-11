from utils.composer.connecting_vowel import ConnectingVowel
from utils.composer.rule import Rule


class AdjectiveWithMonySuffixConnectingVowelRule(Rule):
    def matches(self, left, right):
        return right.orth == "mony"
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]
