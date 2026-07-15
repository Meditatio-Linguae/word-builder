from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.ment import Ment
from utils.composer import ComposingRule


class MentLeftToRightConnectingVowelRule(ComposingRule):
    def __init__(self):
        self.connecting_vowels = ("u", "o", "a")

    def matches(self, left, right):
        return isinstance(right, Ment) and isinstance(left, Base) and not left.orth.endswith(self.connecting_vowels)
    
    def apply(self, left, right):
        return [
            (left, ConnectingVowel(orth=orth), right)
            for orth in self.connecting_vowels
        ]
