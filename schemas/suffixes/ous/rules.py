from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.ous import Ous
from utils.composer import ComposingRule


class OusLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ous) and isinstance(left, Base)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_vowel in ["i", "e"]:
            assimilated.append((left, ConnectingVowel(orth=connecting_vowel), right))
        return assimilated
