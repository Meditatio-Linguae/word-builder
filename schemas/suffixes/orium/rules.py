from schemas.bases import Base
from schemas.suffixes.orium import Orium
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class OriumLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Orium) and isinstance(left, Base)
    
    def apply(self, left, right):
        cloned_right = clone_runtime_object(right)
        cloned_right.orth = cloned_right.orth[:2] + "y"
        return [(left, cloned_right)]
