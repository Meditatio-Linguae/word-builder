from schemas.bases import Base
from schemas.suffixes.rix import Rix
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class RixLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Rix) and isinstance(left, Base) and left.orth.endswith("r")
    
    def apply(self, left, right):
        cloned_right = clone_runtime_object(right)
        cloned_right.orth = cloned_right.orth[1:]
        return [(left, cloned_right)]
