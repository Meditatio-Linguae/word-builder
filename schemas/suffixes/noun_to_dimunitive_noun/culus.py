from schemas.bases import NounBase
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.noun_to_adjective import NounToAdjectiveSuffix
from schemas.suffixes.noun_to_dimunitive_noun import NounToDiminutiveNounSuffix
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class Cule(NounToDiminutiveNounSuffix):
    def __init__(self):
        self.orth = "cule"
        self.meanings = "little"


class Cle(NounToDiminutiveNounSuffix):
    def __init__(self):
        self.orth = "cle"
        self.meanings = "little"


class CuleLeftToRightConnectingVowelRule(ComposingRule):
    def __init__(self):
        self.connecting_vowels = ("i")

    def matches(self, left, right):
        return isinstance(right, (Cule, Cle)) and isinstance(left, NounBase) and (left.declension == 3 or left.declension == 4 or left.declension == 5) and not left.relevant_orth().endswith(self.connecting_vowels)
    
    def apply(self, left, right):
        return [
            (left, ConnectingVowel(orth=orth), right)
            for orth in self.connecting_vowels
        ]
    

class CuleRightToLeftAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(left, Cule) and isinstance(right, NounToAdjectiveSuffix)
    
    def apply(self, left, right):
        cloned_left = clone_runtime_object(left)
        cloned_left.orth = cloned_left.orth[:-1]
        return [(cloned_left, right)]
