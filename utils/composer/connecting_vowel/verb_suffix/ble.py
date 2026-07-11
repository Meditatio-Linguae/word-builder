from schemas.latin.verb import (
    VerbAssimilatedRadicalStem,
    VerbClassNo,
    VerbIrregularPresentInfinitiveStem,
    VerbRegularPerfectParticipleStem, 
    VerbRegularPresentInfinitiveStem,
    VerbStem
)
from utils.composer.connecting_vowel import ConnectingVowel
from utils.composer.rule import Rule


class VerbWithBleSuffixConnectingVowelRule(Rule):
    def matches(self, left, right):
        return right.orth == "ble" and isinstance(left, VerbStem)
    
    def apply(self, left, right):
        vowel = "a" if (hasattr(left, "conjugation_no") and left.conjugation_no == VerbClassNo.I) or (isinstance(left, (VerbIrregularPresentInfinitiveStem, VerbAssimilatedRadicalStem))) else "i"
        return [(left, ConnectingVowel(orth=vowel), right)] if not left.orth.endswith(("a", "i")) else []
