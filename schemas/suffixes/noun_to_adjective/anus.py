from schemas.bases import NounBase
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.noun_to_adjective import NounToAdjectiveSuffix
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class Ane(NounToAdjectiveSuffix):
    def __init__(self):
        self.orth = "ane"
        self.meanings = "pertaining to"


class AneLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ane) and isinstance(left, NounBase)
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]
    

class AneLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ane) and isinstance(left, NounBase)
    
    def apply(self, left, right):
        cloned_right_1 = clone_runtime_object(right)
        cloned_right_1.orth = cloned_right_1.orth[:-1]
        cloned_right_2 = clone_runtime_object(right)
        cloned_right_2.orth = "ain"
        return [
            (left, cloned_right_1),
            (left, cloned_right_2)
        ]
