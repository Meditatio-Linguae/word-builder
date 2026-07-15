from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.lent import Lent
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class LentLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Lent) and isinstance(left, Base)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_vowel in ["u", "o"]:
            assimilated.append((left, ConnectingVowel(orth=connecting_vowel), right))
        return assimilated
