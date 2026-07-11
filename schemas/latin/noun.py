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


class Gender(Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTRAL = "neutral"


class NounClassNo(Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"


class NounStem(Base, Searchable):
    __tablename__ = "noun_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=True)
    declension_no = mapped_column(SQLEnum(NounClassNo, name="noun_class_no"), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="noun_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<NounStem(orth='{self.relevant_orth()}', "
            # f"declension='{self.declension_no}.{self.gender}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )


class NounSuffix(Base, Searchable):
    __tablename__ = "noun_suffix"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=True)
    # converted_pos = mapped_column(SQLEnum(PartOfSpeech, name="converted_pos"), nullable=False)
    declension_required = mapped_column(SQLEnum(NounClassNo, name="noun_class"), nullable=True)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="noun_suffix", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<NounSuffix(orth='{self.relevant_orth()}', "
            # f"convert_to='{self.converted_pos}', "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}')>"
        )
