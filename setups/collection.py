from concurrent.futures import ProcessPoolExecutor
from itertools import chain

from wordfreq import zipf_frequency
from nltk.corpus import wordnet as wn
from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.bases.rules import BaseCompoundConnectingVowelRule, BaseLeftToRightAssimilationRule, BaseRightToLeftAssimilationRule
from schemas.bases import Base
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
from schemas.suffixes.acious import Acious
from schemas.suffixes.acity import Acity
from schemas.suffixes.acy import Acy
from schemas.suffixes.al import Al
from schemas.suffixes.al.rules import AlLeftToRightAssimilationRule, AlLeftToRightConnectingVowelRule
from schemas.suffixes.ane import Ane
from schemas.suffixes.ane.rules import AneLeftToRightAssimilationRule, AneLeftToRightConnectingVowelRule
from schemas.suffixes.arium import Arium
from schemas.suffixes.ary import Ary
from schemas.suffixes.ble import Ble
from schemas.suffixes.ble.rules import (
    BleLeftToRightConnectingVowelRule, 
    BleRightToLeftAssimilationRule
)
from schemas.suffixes.cle.rules import CleLeftToRightConnectingVowelRule
from schemas.suffixes.cule import Cule
from schemas.suffixes.cule.rules import CuleLeftToRightConnectingVowelRule, CuleRightToLeftAssimilationRule
from schemas.suffixes.el import El
from schemas.suffixes.esce import Esce
from schemas.suffixes.ette import Ette
from schemas.suffixes.ette.rules import EtteLeftToRightAssimilationRule
from schemas.suffixes.id import Id
from schemas.suffixes.ine import Ine
from schemas.suffixes.ion import Ion
from schemas.suffixes.itious import Itious
from schemas.suffixes.itude import Itude
from schemas.suffixes.ity import Ity
from schemas.suffixes.ity.rules import ItyLeftToRightAssimilationRule
from schemas.suffixes.ive import Ive
from schemas.suffixes.le import Le
from schemas.suffixes.lence import Lence
from schemas.suffixes.lence.rules import LenceLeftToRightConnectingVowelRule
from schemas.suffixes.lent import Lent
from schemas.suffixes.lent.rules import LentLeftToRightConnectingVowelRule
from schemas.suffixes.men import Men
from schemas.suffixes.men.rules import MenLeftToRightConnectingVowelRule
from schemas.suffixes.ment import Ment
from schemas.suffixes.ment.rules import MentLeftToRightConnectingVowelRule
from schemas.suffixes.mony import Mony
from schemas.suffixes.mony.rules import MonyLeftToRightConnectingVowelRule
from schemas.suffixes.nce import Nce
from schemas.suffixes.nce.rules import NceLeftToRightAssimilationRule
from schemas.suffixes.ncy import Ncy
from schemas.suffixes.ncy.rules import NcyLeftToRightAssimilationRule
from schemas.suffixes.nd import Nd
from schemas.suffixes.nd.rules import NdLeftToRightAssimilationRule
from schemas.suffixes.nt import Nt
from schemas.suffixes.nt.rules import NtLeftToRightAssimilationRule
from schemas.suffixes.or_ import Or
from schemas.suffixes.orium import Orium
from schemas.suffixes.orium.rules import OriumLeftToRightAssimilationRule
from schemas.suffixes.ory import Ory
from schemas.suffixes.ose import Ose
from schemas.suffixes.ose.rules import OseLeftToRightConnectingVowelRule, OseRightToLeftAssimilationRule
from schemas.suffixes.our import Our
from schemas.suffixes.our.rules import OurLeftToRightAssimilationRule
from schemas.suffixes.ous import Ous
from schemas.suffixes.ous.rules import OusLeftToRightConnectingVowelRule
from schemas.suffixes.rix import Rix
from schemas.suffixes.rix.rules import RixLeftToRightAssimilationRule
from schemas.suffixes.ule import Ule
from schemas.suffixes.ule.rules import UleLeftToRightAssimilationRule, UleRightToLeftAssimilationRule
from schemas.suffixes.ulous import Ulous
from schemas.suffixes.uous import Uous
from schemas.suffixes.ure import Ure
from schemas.suffixes.y import Y


class WordBuilder:
    def __init__(self, bases):
        self.prefixes = [
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
        self.bases = bases
        self.suffixes = [
            Acious(),
            Acity(),
            Acy(),
            Al(),
            Ane(),
            Arium(),
            Ary(),
            Ble(),
            Cule(),
            El(),
            Esce(),
            Ette(),
            Id(),
            Ine(),
            Ion(),
            Itious(),
            Itude(),
            Ity(),
            Ive(),
            Le(),
            Lence(),
            Lent(),
            Men(),
            Ment(),
            Mony(),
            Nce(),
            Ncy(),
            Nd(),
            Nt(),
            Or(),
            Orium(),
            Ory(),
            Ose(),
            Our(),
            Ous(),
            Rix(),
            Ule(),
            Ulous(),
            Uous(),
            Ure(),
            Y()
        ]
        self.connecting_vowel_rules = [
            BaseCompoundConnectingVowelRule(),
            BleLeftToRightConnectingVowelRule(),
            MonyLeftToRightConnectingVowelRule(),
            AlLeftToRightConnectingVowelRule(),
            AneLeftToRightConnectingVowelRule(),
            LenceLeftToRightConnectingVowelRule(),
            LentLeftToRightConnectingVowelRule(),
            OusLeftToRightConnectingVowelRule(),
            OseLeftToRightConnectingVowelRule(),
            MentLeftToRightConnectingVowelRule(),
            MenLeftToRightConnectingVowelRule(),
            CuleLeftToRightConnectingVowelRule(),
            CleLeftToRightConnectingVowelRule()
        ]
        self.left_to_right_assimilation_rules = [
            BaseLeftToRightAssimilationRule(),
            ItyLeftToRightAssimilationRule(),
            AlLeftToRightAssimilationRule(),
            AneLeftToRightAssimilationRule(),
            UleLeftToRightAssimilationRule(),
            RixLeftToRightAssimilationRule(),
            OriumLeftToRightAssimilationRule(),
            OurLeftToRightAssimilationRule(),
            EtteLeftToRightAssimilationRule(),
            NceLeftToRightAssimilationRule(),
            NcyLeftToRightAssimilationRule(),
            NdLeftToRightAssimilationRule(),
            NtLeftToRightAssimilationRule(),
        ]
        self.right_to_left_assimilation_rules = [
            BaseRightToLeftAssimilationRule(),
            BleRightToLeftAssimilationRule(),
            AbRightToLeftAssimilationRule(),
            AdRightToLeftAssimilationRule(),
            ComRightToLeftAssimilationRule(),
            DisRightToLeftAssimilationRule(),
            ExRightToLeftAssimilationRule(),
            InRightToLeftAssimilationRule(),
            ObRightToLeftAssimilationRule(),
            ReRightToLeftAssimilationRule(),
            SubRightToLeftAssimilationRule(),
            TransRightToLeftAssimilationRule(),
            UleRightToLeftAssimilationRule(),
            OseRightToLeftAssimilationRule(),
            CuleRightToLeftAssimilationRule(),
        ]

    def compose_word(self, left, right):
        variations = [(left, right)]

        right_to_left_assimilations = []
        for rule in self.right_to_left_assimilation_rules:
            if rule.matches(left, right):
                right_to_left_assimilations.extend(rule.apply(left, right))
        full_assimilations = []
        for right_to_left_assimilation in right_to_left_assimilations:
            for rule in self.left_to_right_assimilation_rules:
                if rule.matches(right_to_left_assimilation[0], right_to_left_assimilation[1]):
                    full_assimilations.extend(rule.apply(right_to_left_assimilation[0], right_to_left_assimilation[1]))
        variations.extend(full_assimilations)

        connecting_vowels = []
        for variation in variations:
            for rule in self.connecting_vowel_rules:
                if rule.matches(variation[0], variation[1]):
                    connecting_vowels.extend(rule.apply(variation[0], variation[1]))
        variations.extend(connecting_vowels)

        return variations
    
    def two_bases_combination(self):
        combinations = []
        for base_left in self.bases:
            for base_right in self.bases:
                for two_bases_combination_ in self.compose_word(base_left, base_right):
                    combinations.append(two_bases_combination_)
        return combinations

    def two_bases_one_suffix_combination(self):
        combinations = []
        for two_bases_combination_ in self.two_bases_combination():
            for suffix in self.suffixes:
                for base_suffix_combination in self.compose_word(two_bases_combination_[1], suffix):
                    combinations.append(two_bases_combination_[:-1] + base_suffix_combination)
        return combinations
    
    def one_base_one_speech_wrapup_combinations(self):
        combinations = []
        for base in self.bases:
            combinations.append((base, E()))
        return combinations
    
    def one_base_one_suffix_combinations(self):
        combinations = []
        for base in self.bases:
            for suffix in self.suffixes:
                for base_suffix_combination in self.compose_word(base, suffix):
                    combinations.append(base_suffix_combination)
        return combinations
    
    def one_base_two_suffixes_combinations(self):
        combinations = []
        for one_base_one_suffix_combination in self.one_base_one_suffix_combinations():
            for suffix in self.suffixes:
                for two_suffixes_combination in self.compose_word(one_base_one_suffix_combination[-1], suffix):
                    combinations.append(one_base_one_suffix_combination[:-1] + two_suffixes_combination)
        return combinations
    
    def one_base_three_suffixes_combinations(self):
        combinations = []
        for one_base_two_suffix_combination in self.one_base_two_suffixes_combinations():
            for suffix in self.suffixes:
                for three_suffixes_combination in self.compose_word(one_base_two_suffix_combination[-1], suffix):
                    combinations.append(one_base_two_suffix_combination[:-1] + three_suffixes_combination)
        return combinations
    
    def one_prefix_one_base_one_speech_wrapup_combinations(self):
        combinations = []
        for base in self.bases:
            for prefix in self.prefixes:
                for prefix_base_combination in self.compose_word(prefix, base):
                    combinations.append(prefix_base_combination + tuple([E()]))
        return combinations
    
    def one_prefix_one_base_one_suffix_combinations(self):
        combinations = [] 
        for base in self.bases:
            for prefix in self.prefixes:
                for prefix_base_combination in self.compose_word(prefix, base):
                    for suffix in self.suffixes:
                        for base_suffix_combination in self.compose_word(prefix_base_combination[-1], suffix):
                            combinations.append(prefix_base_combination[:-1] + base_suffix_combination)
        return combinations
    
    def one_prefix_one_base_two_suffixes_combinations(self):
        combinations = []
        for one_prefix_one_base_one_suffix_combination in self.one_prefix_one_base_one_suffix_combinations():
            for suffix in self.suffixes:
                for two_suffixes_combination in self.compose_word(one_prefix_one_base_one_suffix_combination[-1], suffix):
                    combinations.append(one_prefix_one_base_one_suffix_combination[:-1] + two_suffixes_combination)
        return combinations
    
    def one_prefix_one_base_three_suffixes_combinations(self):
        combinations = []
        for one_prefix_one_base_two_suffixes_combination in self.one_prefix_one_base_two_suffixes_combinations():
            for suffix in self.suffixes:
                for three_suffixes_combination in self.compose_word(one_prefix_one_base_two_suffixes_combination[-1], suffix):
                    combinations.append(one_prefix_one_base_two_suffixes_combination[:-1] + three_suffixes_combination)
        return combinations
    
    def two_prefixes_one_base_two_suffixes_combinations(self):
        combinations = []
        for one_prefix_one_base_two_suffixes_combination in self.one_prefix_one_base_two_suffixes_combinations():
            for prefix in self.prefixes:
                for two_prefixes_combination in self.compose_word(prefix, one_prefix_one_base_two_suffixes_combination[0]):
                    combinations.append(two_prefixes_combination + one_prefix_one_base_two_suffixes_combination[1:])
        return combinations
    
    def two_prefixes_one_base_three_suffixes_combinations(self):
        combinations = []
        for two_prefixes_one_base_three_suffixes_combination in self.two_prefixes_one_base_two_suffixes_combinations():
            for suffix in self.suffixes:
                for two_prefixes_combination in self.compose_word(two_prefixes_one_base_three_suffixes_combination[-1], suffix):
                    combinations.append(two_prefixes_one_base_three_suffixes_combination[:-1] + two_prefixes_combination)
        return combinations


class CollectionBuilder:
    def __init__(self, db_engine, search_engine):
        self.db_engine = db_engine
        self.search_engine = search_engine

    def validate_syntax(self, orth):
        return bool(wn.synsets(orth))
    
    def validate_semantics(self, orth):
        # TODO
        pass
    
    def to_search(self, parts):
        orth = ("".join([part.orth for part in parts]))
        if self.validate_syntax(orth):
            return {
                orth: {
                    "parts": [part.to_searchable() for part in parts]
                }
            }

    def insert_search(self, compounds):
        collection = []
        for compound in compounds:
            to_search = self.to_search(compound)
            if to_search:
                collection.append(to_search)
        self.search_engine.insert_many(collection)
    
    def generate(self):
        with Session(self.db_engine) as session:
            bases = session.scalars(select(Base)).all()
            word_builder = WordBuilder(bases)

            for builder in [
                word_builder.two_bases_combination,
                word_builder.two_bases_one_suffix_combination,
                word_builder.one_base_one_speech_wrapup_combinations,
                word_builder.one_base_one_suffix_combinations,
                word_builder.one_base_two_suffixes_combinations,
                word_builder.one_base_three_suffixes_combinations,
                word_builder.one_prefix_one_base_one_speech_wrapup_combinations,
                word_builder.one_prefix_one_base_one_suffix_combinations,
                word_builder.one_prefix_one_base_two_suffixes_combinations,
                word_builder.one_prefix_one_base_three_suffixes_combinations,
                word_builder.two_prefixes_one_base_two_suffixes_combinations,
                word_builder.two_prefixes_one_base_three_suffixes_combinations,
            ]:
                self.insert_search(builder())
