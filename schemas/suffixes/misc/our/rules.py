from schemas.bases import Base
from schemas.suffixes.misc.our import Our
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class OurLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Our) and isinstance(left, Base)
    
    def apply(self, left, right):
        cloned_right = clone_runtime_object(right)
        cloned_right.orth = "or"
        return [(left, cloned_right)]
