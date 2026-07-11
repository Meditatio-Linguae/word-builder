from schemas.latin.adjective import AdjectiveStem
from schemas.latin.adverb import AdverbStem
from schemas.latin.noun import NounStem
from schemas.latin.preposition import Preposition
from schemas.latin.verb import VerbAssimilatedRadicalStem, VerbIrregularPerfectParticipleStem, VerbIrregularPresentInfinitiveStem, VerbRegularPerfectParticipleStem, VerbRegularPresentInfinitiveStem
from utils.composer.assimilation.left_to_right.adjective import AdjectiveItySuffixAssimilationRule
from utils.composer.assimilation.left_to_right.noun import DropFirstLetterAssimilationRule
from utils.composer.assimilation.left_to_right.ule_suffix import UleAdjectiveFormingSuffixAssimilationRule, UleSuffixCombinationAssimilationRule
from utils.composer.assimilation.left_to_right.verb import VerbAssimilatedRadicalStemAssimilationRule, VerbRegularPerfectParticipleStemAssimilationRule, VerbRegularPresentInfinitiveStemAssimilationRule
from utils.composer.assimilation.right_to_left.prefix import PrefixAssimilationRule
from utils.composer.connecting_vowel.adjective_suffix.mony import AdjectiveWithMonySuffixConnectingVowelRule
from utils.composer.connecting_vowel.compound.dependent import DependentCompoundConnectingVowelRule
from utils.composer.connecting_vowel.compound.descriptive import DescriptiveCompoundConnectingVowelRule
from utils.composer.connecting_vowel.noun_suffix.al import NounWithAlSuffixConnectingVowelRule
from utils.composer.connecting_vowel.noun_suffix.cle import NounWithCleSuffixConnectingVowelRule
from utils.composer.connecting_vowel.noun_suffix.lent import NounWithLentSuffixConnectingVowelRule
from utils.composer.connecting_vowel.verb_suffix.ble import VerbWithBleSuffixConnectingVowelRule
from utils.composer.connecting_vowel.verb_suffix.men import VerbWithMenSuffixConnectingVowelRule
from utils.composer.connecting_vowel.verb_suffix.ment import VerbWithMentSuffixConnectingVowelRule
from utils.composer.connecting_vowel.verb_suffix.nt import VerbWithNtSuffixAssimilationRule


ASSIMILATION_RULES = [
    VerbAssimilatedRadicalStemAssimilationRule(),
    VerbRegularPresentInfinitiveStemAssimilationRule(),
    VerbRegularPerfectParticipleStemAssimilationRule(),
    PrefixAssimilationRule(),
    DropFirstLetterAssimilationRule(),
    AdjectiveItySuffixAssimilationRule(),
    VerbWithNtSuffixAssimilationRule(),
    UleAdjectiveFormingSuffixAssimilationRule(),
    UleSuffixCombinationAssimilationRule()
]

CONNECTING_VOWEL_RULES = [
    VerbWithBleSuffixConnectingVowelRule(),
    VerbWithMenSuffixConnectingVowelRule(),
    VerbWithMentSuffixConnectingVowelRule(),
    AdjectiveWithMonySuffixConnectingVowelRule(),
    NounWithAlSuffixConnectingVowelRule(),
    NounWithCleSuffixConnectingVowelRule(),
    NounWithLentSuffixConnectingVowelRule(),
    DependentCompoundConnectingVowelRule(),
    DescriptiveCompoundConnectingVowelRule()
]
    

def compose_word(left, right):
    variations = [(left, right)]
    print(variations)

    assimilation = []
    for rule in ASSIMILATION_RULES:
        if rule.matches(left, right):
            assimilation.extend(rule.apply(left, right))
    variations.extend(assimilation)

    connecting_vowels = []
    for cloned_left, cloned_right in variations:
        for rule in CONNECTING_VOWEL_RULES:
            if rule.matches(cloned_left, cloned_right):
                connecting_vowels.extend(rule.apply(cloned_left, cloned_right))
    variations.extend(connecting_vowels)

    return variations
