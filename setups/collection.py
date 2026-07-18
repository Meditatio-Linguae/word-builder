from wordfreq import zipf_frequency
from nltk.corpus import wordnet as wn
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.bases import NounBase
from schemas.prefixes.ab import Ab
from schemas.prefixes.ab.rules import AbRightToLeftAssimilationRule
from schemas.prefixes.ad import Ad
from schemas.prefixes.ad.rules import AdRightToLeftAssimilationRule
from schemas.prefixes.ambi import Ambi
from schemas.prefixes.ante import Ante
from schemas.prefixes.circum import Circum
from schemas.prefixes.com import Com
from schemas.prefixes.com.rules import ComRightToLeftAssimilationRule
from schemas.prefixes.contra import Contra
from schemas.prefixes.contro import Contro
from schemas.prefixes.counter import Counter
from schemas.prefixes.de import De
from schemas.prefixes.dis import Dis
from schemas.prefixes.dis.rules import DisRightToLeftAssimilationRule
from schemas.prefixes.ex import Ex
from schemas.prefixes.ex.rules import ExRightToLeftAssimilationRule
from schemas.prefixes.extra import Extra
from schemas.prefixes.extro import Extro
from schemas.prefixes.in_ import In
from schemas.prefixes.in_.rules import InRightToLeftAssimilationRule
from schemas.prefixes.infra import Infra
from schemas.prefixes.inter import Inter
from schemas.prefixes.intra import Intra
from schemas.prefixes.intro import Intro
from schemas.prefixes.non import Non
from schemas.prefixes.ob import Ob
from schemas.prefixes.ob.rules import ObRightToLeftAssimilationRule
from schemas.prefixes.per import Per
from schemas.prefixes.post import Post
from schemas.prefixes.pre import Pre
from schemas.prefixes.pro import Pro
from schemas.prefixes.re import Re
from schemas.prefixes.re.rules import ReRightToLeftAssimilationRule
from schemas.prefixes.retro import Retro
from schemas.prefixes.se import Se
from schemas.prefixes.sed import Sed
from schemas.prefixes.sub import Sub
from schemas.prefixes.sub.rules import SubRightToLeftAssimilationRule
from schemas.prefixes.super import Super
from schemas.prefixes.trans import Trans
from schemas.prefixes.trans.rules import TransRightToLeftAssimilationRule
from schemas.prefixes.ultra import Ultra
from schemas.speech_wrapup import E
from schemas.suffixes.noun_to_adjective import alis, anus, arium, ilis, inus, lentus, osus
from schemas.suffixes.noun_to_dimunitive_noun import culus, ellus, ulus


def compose_word(
        left, 
        right, 
        connecting_vowel_rules, 
        left_to_right_assimilation_rules, 
        right_to_left_assimilation_rules
    ):
    variations = [(left, right)]

    right_to_left_assimilations = []
    for rule in right_to_left_assimilation_rules:
        if rule.matches(left, right):
            right_to_left_assimilations.extend(rule.apply(left, right))
    full_assimilations = []
    for right_to_left_assimilation in right_to_left_assimilations:
        for rule in left_to_right_assimilation_rules:
            if rule.matches(right_to_left_assimilation[0], right_to_left_assimilation[1]):
                full_assimilations.extend(rule.apply(right_to_left_assimilation[0], right_to_left_assimilation[1]))
    variations.extend(full_assimilations)

    connecting_vowels = []
    for variation in variations:
        for rule in connecting_vowel_rules:
            if rule.matches(variation[0], variation[1]):
                connecting_vowels.extend(rule.apply(variation[0], variation[1]))
    variations.extend(connecting_vowels)

    return variations


class Affix:
    def __init__(
            self, 
            base, 
            connecting_vowel_rules=[], 
            left_to_right_assimilation_rules=[], 
            right_to_left_assimilation_rules=[]
        ):
        self.base = base
        self.connecting_vowel_rules = connecting_vowel_rules
        self.left_to_right_assimilation_rules = left_to_right_assimilation_rules
        self.right_to_left_assimilation_rules = right_to_left_assimilation_rules

    def __repr__(self):
        return f"<Affix(base='{self.base}')"


class WordBuilder:
    def __init__(self, bases):
        self.bases = bases
    
    def one_base_one_suffix(self, suffix):
        combinations = []
        for base in self.bases:
            for base_suffix_combination in \
                compose_word(
                    left=base, 
                    right=suffix.base, 
                    connecting_vowel_rules=suffix.connecting_vowel_rules, 
                    left_to_right_assimilation_rules=suffix.left_to_right_assimilation_rules, 
                    right_to_left_assimilation_rules=suffix.right_to_left_assimilation_rules
                ):
                combinations.append(base_suffix_combination)
        return combinations
    
    def one_base_two_suffixes(self, first_suffix, second_suffix):
        combinations = []
        for one_base_two_suffixes_combination in self.one_base_one_suffix(first_suffix):
            for two_suffixes_combination in \
                compose_word(
                    left=one_base_two_suffixes_combination[-1], 
                    right=second_suffix.base,
                    connecting_vowel_rules=second_suffix.connecting_vowel_rules,
                    left_to_right_assimilation_rules=second_suffix.left_to_right_assimilation_rules,
                    right_to_left_assimilation_rules=second_suffix.right_to_left_assimilation_rules
                ):
                combinations.append(one_base_two_suffixes_combination[:-1] + two_suffixes_combination)
        return combinations


class CollectionBuilder:
    def __init__(self, db_engine, search_engine):
        self.db_engine = db_engine
        self.search_engine = search_engine

    def validate_syntax(self, orth):
        return bool(wn.synsets(orth))
    
    def to_search(self, parts):
        orth = ("".join([part.relevant_orth() for part in parts]))
        if self.validate_syntax(orth):
            return {
                orth: {
                    "parts": [part.to_searchable() for part in parts]
                }
            }

    def search_insert(self, compounds):
        collection = []
        for compound in compounds:
            to_search = self.to_search(compound)
            if to_search:
                collection.append(to_search)
        if len(collection) > 0:
            self.search_engine.insert_many(collection)
    
    def generate(self):
        with Session(self.db_engine) as session:
            noun_bases = session.scalars(select(NounBase)).all()
            word_builder = WordBuilder(noun_bases)

            noun_to_adjective_suffixes = [
                Affix(
                    base=alis.Al(),
                    connecting_vowel_rules=[alis.AlLeftToRightConnectingVowelRule()],
                    left_to_right_assimilation_rules=[alis.AlLeftToRightAssimilationRule()]
                ),
                Affix(
                    base=anus.Ane(),
                    connecting_vowel_rules=[anus.AneLeftToRightConnectingVowelRule()],
                    left_to_right_assimilation_rules=[anus.AneLeftToRightAssimilationRule()]
                ),
                Affix(base=arium.Arium()),
                Affix(base=arium.Ary()),
                Affix(base=inus.Ine()),
                Affix(base=ilis.Ile()),
                Affix(base=ilis.Il()),
                Affix(
                    base=lentus.Lent(),
                    connecting_vowel_rules=[lentus.LentLeftToRightConnectingVowelRule()]
                ),
                Affix(
                    base=osus.Ose(),
                    connecting_vowel_rules=[osus.OseLeftToRightConnectingVowelRule()],
                    right_to_left_assimilation_rules=[osus.OseRightToLeftAssimilationRule()],
                ),
                Affix(
                    base=osus.Ous(),
                    connecting_vowel_rules=[osus.OusLeftToRightConnectingVowelRule()],
                )
            ]

            # for noun_to_adjective_suffix in noun_to_adjective_suffixes:
            #     results = word_builder.one_base_one_suffix(noun_to_adjective_suffix)
            #     self.search_insert(results)


            noun_to_diminutive_noun_suffixes = [
                Affix(
                    base=culus.Cule(),
                    connecting_vowel_rules=[culus.CuleLeftToRightConnectingVowelRule()],
                    right_to_left_assimilation_rules=[culus.CuleRightToLeftAssimilationRule()]
                ),
                Affix(
                    base=culus.Cle(),
                    connecting_vowel_rules=[culus.CuleLeftToRightConnectingVowelRule()]
                ),
                Affix(
                    base=ulus.Ule(),
                    left_to_right_assimilation_rules=[ulus.UleLeftToRightAssimilationRule()],
                    right_to_left_assimilation_rules=[ulus.UleRightToLeftAssimilationRule()]
                )
            ]

            for noun_to_diminutive_noun_suffix in noun_to_diminutive_noun_suffixes:
                for noun_to_adjective_suffix in noun_to_adjective_suffixes:
                    results = word_builder.one_base_two_suffixes(noun_to_diminutive_noun_suffix, noun_to_adjective_suffix)
                    self.search_insert(results)


            prefixes = [
                Ab(),
                Ad(),
                Ambi(),
                Ante(),
                Circum(),
                Com(),
                Contra(),
                Contro(),
                Counter(),
                De(),
                Dis(),
                Ex(),
                Extra(),
                Extro(),
                In(),
                Infra(),
                Inter(),
                Intra(),
                Intro(),
                Non(),
                Ob(),
                Per(),
                Post(),
                Pre(),
                Pro(),
                Re(),
                Retro(),
                Se(),
                Sed(),
                Sub(),
                Super(),
                Trans(),
                Ultra()
            ]


