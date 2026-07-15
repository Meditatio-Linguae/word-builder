from utils.composer import ComposingRule
from utils.misc import clone_runtime_object
from utils.search import Searchable


class Prefix(Searchable):
    pass


class PrefixComposingRule(ComposingRule):
    def __init__(self):
        self.rules = []

    def apply(self, left, right):
        cloned_left = clone_runtime_object(left)
        cloned_right = clone_runtime_object(right)

        for condition, transform in self.rules:
            if right.orth.startswith(condition):
                cloned_left.orth = transform(cloned_left.orth, cloned_right.orth)
                return [(cloned_left, cloned_right)]
            
        return []
