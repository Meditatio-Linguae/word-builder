from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes import Suffix
from schemas.suffixes.al import Al
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class AlLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Al) and isinstance(left, Base)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_vowel in ["i", "e"]:
            assimilated.append((left, ConnectingVowel(orth=connecting_vowel), right))
        return assimilated


class AlLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Al) and isinstance(left, (Base, Suffix)) and "l" in left.orth
    
    def apply(self, left, right):
        cloned_right = clone_runtime_object(right)
        cloned_right.orth = cloned_right.orth[:-1] + "r"
        return [(left, cloned_right)]
