from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.men import Men
from utils.composer import ComposingRule


class MenLeftToRightConnectingVowelRule(ComposingRule):
    def __init__(self):
        self.connecting_vowels = ("i")

    def matches(self, left, right):
        return isinstance(right, Men) and isinstance(left, Base) and not left.orth.endswith(self.connecting_vowels)
    
    def apply(self, left, right):
        return [
            (left, ConnectingVowel(orth=orth), right)
            for orth in self.connecting_vowels
        ]
