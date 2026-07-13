from schemas.bases import Base
from schemas.suffixes import Suffix
from schemas.suffixes.ule import Ule
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class UleLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ule) and isinstance(left, Base)
    
    def apply(self, left, right):
        cloned_right = clone_runtime_object(right)
        cloned_right.orth = "o" + cloned_right.orth[1:]
        return [(left, cloned_right)]


class UleRightToLeftAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(left, Ule) and isinstance(right, Suffix)
    
    def apply(self, left, right):
        cloned_left = clone_runtime_object(left)
        cloned_left.orth = cloned_left.orth[:-1]
        return [(cloned_left, right)]
