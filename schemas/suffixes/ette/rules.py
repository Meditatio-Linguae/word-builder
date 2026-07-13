from schemas.bases import Base
from schemas.suffixes.ette import Ette
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class EtteLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ette) and isinstance(left, Base)
    
    def apply(self, left, right):
        cloned_right = clone_runtime_object(right)
        cloned_right.orth = cloned_right.orth[:2]
        return [(left, cloned_right)]
