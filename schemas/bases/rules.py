from schemas.bases import Base
from schemas.connecting_vowel import ConnectingVowel
from schemas.prefixes import Prefix
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class BaseCompoundConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(left, Base) and isinstance(right, Base) and not right.orth.startswith(("a", "e", "i", "o", "u"))
    
    def apply(self, left, right):
        return [
            (left, ConnectingVowel(orth="u"), right),
            (left, ConnectingVowel(orth="i"), right),
            (left, ConnectingVowel(orth="e"), right),
            (left, ConnectingVowel(orth="o"), right)
        ]
    

class BaseLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Base)
    
    def apply(self, left, right):
        if left.orth.endswith("x") and right.orth.startswith("s"):
            cloned_right = clone_runtime_object(right)
            cloned_right.orth = cloned_right.orth[1:]
            return [(left, cloned_right)]
        #     if to_orth in ["e"]:
        #         if orth.endswith("ti"):
        #             base.radical.orth = orth[:len(orth) - 2] + "c"
        #     if to_orth in ["y"]:
        #         if orth.endswith("i"):
        #             base.radical.orth = orth[:len(orth) - 1]
            
        #     return [base] + other_bases

        return []


class BaseRightToLeftAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(left, Base)
    
    def apply(self, left, right):
        if left.orth.endswith("y"):
            cloned_left = clone_runtime_object(left)
            cloned_left.orth = cloned_left.orth[:-1] + "i"
            return [(cloned_left, right)]
        
        return []
