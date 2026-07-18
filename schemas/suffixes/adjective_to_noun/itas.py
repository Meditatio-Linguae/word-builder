from schemas.bases import AdjectiveBase
from schemas.suffixes import Suffix
from schemas.suffixes.adjective_to_noun.itas import Ity
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class Ity(Suffix):
    def __init__(self):
        self.orth = "ity"
        self.meanings = "quality of"


class ItyLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ity) and isinstance(left, AdjectiveBase) and (left.orth.endswith("i") or left.orth.endswith("r"))
    
    def apply(self, left, right):
        cloned_right = clone_runtime_object(right)

        if left.orth.endswith("i"):
            cloned_right.orth = "e" + cloned_right.orth[1:]
        elif left.orth.endswith("r"):
            cloned_right.orth = cloned_right.orth[1:]
        
        return [(left, cloned_right)]
