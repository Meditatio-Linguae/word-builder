from enum import Enum
from sqlalchemy import (
    Integer,
    String,
    Enum as SQLEnum
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base import Base
from utils.search import Searchable


class CountryCode(Enum):
    LA = "la"
    EL = "el"
    EN = "en"
    FR = "fr"


class Radical(Base, Searchable):
    __tablename__ = "radical"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    meanings = mapped_column(String(255), nullable=False)
    origin_of_tongue = mapped_column(SQLEnum(CountryCode, name="country_code"), nullable=False)

    verb_assimilated_radical_stem: Mapped["VerbAssimilatedRadicalStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    verb_regular_present_infinitive_stem: Mapped["VerbRegularPresentInfinitiveStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    verb_regular_perfect_participle_stem: Mapped["VerbRegularPerfectParticipleStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    verb_irregular_present_infinitive_stem: Mapped["VerbIrregularPresentInfinitiveStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    verb_irregular_perfect_participle_stem: Mapped["VerbIrregularPerfectParticipleStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    noun_stem: Mapped["NounStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    adjective_positive_stem: Mapped["AdjectivePositiveStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    adjective_comparative_stem: Mapped["AdjectiveComparativeStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    adjective_superlative_stem: Mapped["AdjectiveSuperlativeStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    adjective_numeral_stem: Mapped["AdjectiveNumeralStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    adverb_stem: Mapped["AdverbStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    # pronounce_stem: Mapped["PronounceStem"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    verb_present_infinitive_suffix: Mapped["VerbPresentInfinitiveSuffix"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    verb_perfect_participle_suffix: Mapped["VerbPerfectParticipleSuffix"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    verb_assimilated_radical_suffix: Mapped["VerbAssimilatedRadicalSuffix"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    adjective_suffix: Mapped["AdjectiveSuffix"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    noun_suffix: Mapped["NounSuffix"] = relationship(back_populates="radical", cascade="all, delete-orphan")
    preposition: Mapped["Preposition"] = relationship(back_populates="radical", cascade="all, delete-orphan")

    def to_searchable(self):
        return super().to_searchable(
            root_orth=self.orth,
            meanings=self.meanings,
            origin_of_tongue=self.origin_of_tongue.value
        )

    def __repr__(self):
        return f"<Radical(orth='{self.orth}', origin_of_tongue={self.origin_of_tongue.value}', meaning='{self.meanings})>"