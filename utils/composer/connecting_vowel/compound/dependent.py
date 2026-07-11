from schemas.latin.adjective import AdjectiveStem
from schemas.latin.adverb import AdverbStem
from schemas.latin.noun import NounStem
from schemas.latin.verb import (
    VerbAssimilatedRadicalStem,
    VerbIrregularPerfectParticipleStem,
    VerbRegularPerfectParticipleStem
)
from utils.composer.connecting_vowel import ConnectingVowel
from utils.composer.rule import Rule


class DependentCompoundConnectingVowelRule(Rule):
    def matches(self, left, right):
        return isinstance(right, (VerbAssimilatedRadicalStem, VerbRegularPerfectParticipleStem, VerbIrregularPerfectParticipleStem)) and isinstance(left, (AdjectiveStem, NounStem, AdverbStem))
    
    def apply(self, left, right):
        return [
            (left, ConnectingVowel(orth="u"), right),
            (left, ConnectingVowel(orth="i"), right),
            (left, ConnectingVowel(orth="e"), right)
        ]
