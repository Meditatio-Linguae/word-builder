from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.mony import Mony
from utils.composer import ComposingRule


class MonyLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Mony) and isinstance(left, Base) and not left.orth.endswith("i")
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]
