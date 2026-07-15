from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.lence import Lence
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class LenceLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Lence) and isinstance(left, Base)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_vowel in ["u", "o"]:
            assimilated.append((left, ConnectingVowel(orth=connecting_vowel), right))
        return assimilated
