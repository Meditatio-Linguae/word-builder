from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes import Suffix
from schemas.suffixes.cule import Cule
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class CuleLeftToRightConnectingVowelRule(ComposingRule):
    def __init__(self):
        self.connecting_vowels = ("i")

    def matches(self, left, right):
        return isinstance(right, Cule) and isinstance(left, Base) and not left.orth.endswith(self.connecting_vowels)
    
    def apply(self, left, right):
        return [
            (left, ConnectingVowel(orth=orth), right)
            for orth in self.connecting_vowels
        ]
    

class CuleRightToLeftAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(left, Cule) and isinstance(right, Suffix)
    
    def apply(self, left, right):
        cloned_left = clone_runtime_object(left)
        cloned_left.orth = "cul"
        return [(cloned_left, right)]