from schemas.bases import Base
from schemas.suffixes.nd import Nd
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class NdLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Nd) and isinstance(left, Base)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_orth in ("a", "e", "ie"):
            cloned_right_1 = clone_runtime_object(right)
            cloned_right_1.orth = connecting_orth + cloned_right_1.orth
            assimilated.append((left, cloned_right_1))
            cloned_right_2 = clone_runtime_object(right)
            cloned_right_2.orth = connecting_orth + cloned_right_2.orth + "um"
            assimilated.append((left, cloned_right_2))
        return assimilated
