from schemas.bases import NounBase
from schemas.suffixes.noun_to_adjective import NounToAdjectiveSuffix
from schemas.suffixes.noun_to_dimunitive_noun import NounToDiminutiveNounSuffix
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class Ule(NounToDiminutiveNounSuffix):
    def __init__(self):
        self.orth = "ule"
        self.meanings = "little"


class UleLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ule) and isinstance(left, NounBase) and (left.declension == 1 or left.declension == 2) and left.relevant_orth().endswith(("e", "i", "u"))
    
    def apply(self, left, right):
        cloned_right = clone_runtime_object(right)
        cloned_right.orth = "o" + cloned_right.orth[1:]
        return [(left, cloned_right)]


class UleRightToLeftAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(left, Ule) and isinstance(right, NounToAdjectiveSuffix)
    
    def apply(self, left, right):
        cloned_left = clone_runtime_object(left)
        cloned_left.orth = cloned_left.orth[:-1]
        return [(cloned_left, right)]