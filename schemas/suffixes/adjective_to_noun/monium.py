from schemas.bases import AdjectiveBase
from schemas.connecting_vowel import ConnectingVowel
from schemas.suffixes.adjective_to_noun import AdjectiveToNounSuffix
from schemas.suffixes.adjective_to_noun.monium import Mony
from utils.composer import ComposingRule


class Mony(AdjectiveToNounSuffix):
    def __init__(self):
        self.orth = "mony"
        self.meanings = "quality of"


class MonyLeftToRightConnectingVowelRule(ComposingRule):
    def matches(self, left, right):
        return isinstance(right, Mony) and isinstance(left, AdjectiveBase) and not left.orth.endswith("i")
    
    def apply(self, left, right):
        return [(left, ConnectingVowel(orth="i"), right)]