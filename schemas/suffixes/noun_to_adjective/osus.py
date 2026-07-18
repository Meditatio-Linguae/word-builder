from schemas.bases import NounBase
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.adjective_to_noun import AdjectiveToNounSuffix
from schemas.suffixes.noun_to_adjective import NounToAdjectiveSuffix
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class Ose(NounToAdjectiveSuffix):
    def __init__(self):
        self.orth = "ose"
        self.meanings = "full of"


class OseLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ose) and isinstance(left, NounBase)
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]
    

class OseRightToLeftAssimilationRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(left, Ose) and isinstance(right, (AdjectiveToNounSuffix))
    
    def apply(self, left, right):
        cloned_left = clone_runtime_object(left)
        cloned_left.orth = cloned_left.orth[:-1]
        return [(cloned_left, right)]


class Ous(NounToAdjectiveSuffix):
    def __init__(self):
        self.orth = "ous"
        self.meanings = "full of"


class OusLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Ous) and isinstance(left, NounBase)
    
    def apply(self, left, right):
        assimilated = []
        for connecting_vowel in ["i", "e"]:
            assimilated.append((left, ConnectingVowel(orth=connecting_vowel), right))
        return assimilated
