from enum import Enum

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    ForeignKey,
    Enum as SQLEnum
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
import spacy
import pyinflect

from .base import Base
from utils.search import Searchable


class VerbClassNo(Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"


class VerbStem(Searchable):
    def relevant_meanings(self):
        meanings = self.radical.meanings
        
        if isinstance(self, VerbRegularPresentInfinitiveStem) or isinstance(self, VerbIrregularPresentInfinitiveStem):
            meanings = meanings.split(", ")
            meanings = "".join([
                f"to {meaning}{', ' if i != len(meanings) - 1 else ''}" 
                for i, meaning in enumerate(meanings)
            ])
        elif isinstance(self, VerbRegularPerfectParticipleStem) or isinstance(self, VerbIrregularPerfectParticipleStem):
            meanings = meanings.split(", ")
            nlp = spacy.load("en_core_web_sm")
            meanings = "".join([
                f"have been {nlp(meaning)[0]._.inflect('VBN')} {' '.join(meaning.split(' ')[1:])}{', ' if i != len(meanings) - 1 else ''}" 
                for i, meaning in enumerate(meanings)
            ])

        return meanings
    
    def to_searchable(self):
        return super().to_searchable(
            orth=self.relevant_orth(),
            meanings=self.relevant_meanings()
        )
    

class VerbAssimilatedRadicalStem(Base, VerbStem):
    __tablename__ = "verb_assimilated_radical_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="verb_assimilated_radical_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<VerbAssimilatedRadicalStem(orth='{self.relevant_orth()}'), "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}'>"
        )


class VerbRegularPresentInfinitiveStem(Base, VerbStem):
    __tablename__ = "verb_regular_present_infinitive_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    conjugation_no = mapped_column(SQLEnum(VerbClassNo, name="verb_class_no"), nullable=False)
    is_istem = mapped_column(Boolean, nullable=False, default=False)
    is_deponent = mapped_column(Boolean, nullable=False, default=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="verb_regular_present_infinitive_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<VerbRegularPresentInfinitiveStem(orth='{self.relevant_orth()}', "
            f"conjugation='{self.conjugation_no.value}.{'i-stem' if self.is_istem else ''}.{'deponent' if self.is_deponent else ''}', "
            f"meanings='{self.relevant_meanings()}')>"
        )
    

class VerbIrregularPresentInfinitiveStem(Base, VerbStem):
    __tablename__ = "verb_irregular_present_infinitive_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="verb_irregular_present_infinitive_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return f"<VerbIrregularPresentInfinitiveStem(orth='{self.relevant_orth()}', meanings='{self.relevant_meanings()}')>"


class VerbPresentInfinitiveSuffix(Base, Searchable):
    __tablename__ = "verb_present_infinitive_suffix"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    # converted_pos = mapped_column(SQLEnum(PartOfSpeech, name="converted_pos"), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="verb_present_infinitive_suffix", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<VerbPresentInfinitiveSuffix(orth='{self.relevant_orth()}', "
            # f"convert_to='{self.converted_pos}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )


class VerbRegularPerfectParticipleStem(Base, VerbStem):
    __tablename__ = "verb_regular_perfect_participle_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    conjugation_no = mapped_column(SQLEnum(VerbClassNo, name="verb_class_no"), nullable=False)
    is_istem = mapped_column(Boolean, nullable=False, default=False)
    is_deponent = mapped_column(Boolean, nullable=False, default=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="verb_regular_perfect_participle_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<VerbRegularPerfectParticipleStem(orth='{self.relevant_orth()}', "
            f"conjugation='{self.conjugation_no.value}.{'i-stem' if self.is_istem else ''}.{'deponent' if self.is_deponent else ''}', "
            f"meanings='{self.relevant_meanings()}')>"
        )
    

class VerbIrregularPerfectParticipleStem(Base, VerbStem):
    __tablename__ = "verb_irregular_perfect_participle_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="verb_irregular_perfect_participle_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return f"<VerbIrregularPerfectParticipleStem(orth='{self.relevant_orth()}', meanings='{self.relevant_meanings()}')>"


class VerbPerfectParticipleSuffix(Base, Searchable):
    __tablename__ = "verb_perfect_participle_suffix"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=True)
    # converted_pos = mapped_column(SQLEnum(PartOfSpeech, name="converted_pos"), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="verb_perfect_participle_suffix", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<VerbPerfectParticipleSuffix(orth='{self.relevant_orth()}', "
            # f"convert_to='{self.converted_pos}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )
    

class VerbAssimilatedRadicalSuffix(Base, Searchable):
    __tablename__ = "verb_assimilated_radical_suffix"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=True)
    # converted_pos = mapped_column(SQLEnum(PartOfSpeech, name="converted_pos"), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="verb_assimilated_radical_suffix", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<VerbRadicalSuffix(orth='{self.relevant_orth()}', "
            # f"convert_to='{self.converted_pos}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )