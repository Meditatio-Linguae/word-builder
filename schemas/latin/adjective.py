from enum import Enum
from sqlalchemy import (
    Integer,
    String,
    Enum as SQLEnum,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .base import Base
from utils.search import Searchable


class Degree(Enum):
    POSITIVE = "positive"
    COMPARATIVE = "comparative"
    SUPERLATIVE = "superlative"
    NUMERAL = "numeral"


class AdjectiveClassNo(Enum):
    I = "I"
    II = "II"
    III = "III"
    IRREGULAR = "Irregular"


class AdjectiveStem:
    pass


class AdjectivePositiveStem(Base, AdjectiveStem, Searchable):
    __tablename__ = "positive_adjective_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    declension_no = mapped_column(SQLEnum(AdjectiveClassNo, name="adjective_class_no"), nullable=True)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="adjective_positive_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<AdjectivePositiveStem(orth='{self.relevant_orth()}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )
    

class AdjectiveComparativeStem(Base, AdjectiveStem, Searchable):
    __tablename__ = "comparative_adjective_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="adjective_comparative_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<AdjectiveComparativeStem(orth='{self.relevant_orth()}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )
    

class AdjectiveSuperlativeStem(Base, AdjectiveStem, Searchable):
    __tablename__ = "superlative_adjective_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="adjective_superlative_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<AdjectiveSuperlativeStem(orth='{self.relevant_orth()}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )
    

class AdjectiveNumeralStem(Base, AdjectiveStem, Searchable):
    __tablename__ = "numeral_adjective_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="adjective_numeral_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<NumeralAdjectiveStem(orth='{self.relevant_orth()}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )


class AdjectiveSuffix(Base, Searchable):
    __tablename__ = "adjective_suffix"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    # converted_pos = mapped_column(SQLEnum(PartOfSpeech, name="converted_pos"), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="adjective_suffix", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<AdjectiveSuffix(orth='{self.relevant_orth()}', "
            f"convert_to='{self.converted_pos}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )