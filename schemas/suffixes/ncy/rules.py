from schemas.bases import Base
from schemas.suffixes.ncy import Ncy
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class NcyLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ncy) and isinstance(left, Base)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_orth in ("a", "e", "ie"):
            cloned_right = clone_runtime_object(right)
            cloned_right.orth = connecting_orth + cloned_right.orth
            assimilated.append((left, cloned_right))
        return assimilated
