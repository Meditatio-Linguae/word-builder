from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes import Suffix
from schemas.suffixes.ose import Ose
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class OseLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ose) and isinstance(left, Base)
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]
    

class OseRightToLeftAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(left, Ose) and isinstance(right, Suffix)
    
    def apply(self, left, right):
        cloned_left = clone_runtime_object(left)
        cloned_left.orth = cloned_left.orth[:-1]
        return [(cloned_left, right)]
