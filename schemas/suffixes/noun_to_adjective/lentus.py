from schemas.bases import NounBase
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.noun_to_adjective import NounToAdjectiveSuffix
from utils.composer import ComposingRule


class Lent(NounToAdjectiveSuffix):
    def __init__(self):
        self.orth = "lent"
        self.meanings = "full of"


class LentLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Lent) and isinstance(left, NounBase)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_vowel in ["u", "o"]:
            assimilated.append((left, ConnectingVowel(orth=connecting_vowel), right))
        return assimilated
