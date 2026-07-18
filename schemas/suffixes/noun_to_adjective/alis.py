from schemas.bases import NounBase
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.noun_to_adjective import NounToAdjectiveSuffix
from schemas.suffixes.noun_to_dimunitive_noun import NounToDiminutiveNounSuffix
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class Al(NounToAdjectiveSuffix):
    def __init__(self):
        self.orth = "al"
        self.meanings = "pertaining to"


class AlLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Al) and isinstance(left, NounBase)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_vowel in ["i", "e"]:
            assimilated.append((left, ConnectingVowel(orth=connecting_vowel), right))
        return assimilated


class AlLeftToRightAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Al) and isinstance(left, (NounBase, NounToDiminutiveNounSuffix)) and "l" in left.relevant_orth()
    
    def apply(self, left, right):
        cloned_right_1 = clone_runtime_object(right)
        cloned_right_1.orth = cloned_right_1.orth[:-1] + "r"
        cloned_right_2 = clone_runtime_object(right)
        cloned_right_2.orth = cloned_right_2.orth[:-1] + "ry"
        return [(left, cloned_right_1), (left, cloned_right_2)]