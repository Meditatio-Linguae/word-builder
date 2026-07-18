from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from schemas.database import Database
from utils.search import Searchable


class Base(Database):
    __tablename__ = "base"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    meanings = mapped_column(String(255), nullable=False)

    noun_base: Mapped["NounBase"] = relationship(back_populates="base", cascade="all, delete-orphan")
    adjective_base: Mapped["AdjectiveBase"] = relationship(back_populates="base", cascade="all, delete-orphan")
    verb_regular_present_infinitive_base: Mapped["VerbRegularPresentInfinitiveBase"] = relationship(back_populates="base", cascade="all, delete-orphan")
    verb_regular_perfect_participle_base: Mapped["VerbRegularPerfectParticipleBase"] = relationship(back_populates="base", cascade="all, delete-orphan")
    verb_irregular_present_infinitive_base: Mapped["VerbIrregularPresentInfinitiveBase"] = relationship(back_populates="base", cascade="all, delete-orphan")
    verb_irregular_perfect_participle_base: Mapped["VerbIrregularPerfectParticipleBase"] = relationship(back_populates="base", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Base(orth='{self.orth}', meaning='{self.meanings}')>"
    

class NounBase(Database, Searchable):
    __tablename__ = "noun_base"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    declension = mapped_column(Integer, nullable=False)
    base_id = mapped_column(Integer, ForeignKey("base.id"), nullable=False)

    base: Mapped["Base"] = relationship(back_populates="noun_base", foreign_keys=[base_id])

    def __repr__(self):
        return f"<NounBase(orth='{self.base.orth}', declension='{self.declension}', meaning='{self.base.meanings}')>"
    

class AdjectiveBase(Database, Searchable):
    __tablename__ = "adjective_base"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_id = mapped_column(Integer, ForeignKey("base.id"), nullable=False)

    base: Mapped["Base"] = relationship(back_populates="adjective_base", foreign_keys=[base_id])

    def __repr__(self):
        return f"<AdjectiveBase(orth='{self.base.orth}', meaning='{self.base.meanings}')>"
    

class VerbRegularPresentInfinitiveBase(Database, Searchable):
    __tablename__ = "verb_regular_present_infinitive_base"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    conjugation = mapped_column(Integer, nullable=False)
    i_stem = mapped_column(Boolean, nullable=False, default=False)
    deponent = mapped_column(Boolean, nullable=False, default=False)
    base_id = mapped_column(Integer, ForeignKey("base.id"), nullable=False)

    base: Mapped["Base"] = relationship(back_populates="verb_regular_present_infinitive_base", foreign_keys=[base_id])

    def __repr__(self):
        return (
            f"<VerbRegularPresentInfinitiveBase(orth='{self.base.orth}', "
            f"conjugation='{self.conjugation}.{'i-stem' if self.i_stem else ''}.{'deponent' if self.deponent else ''}', "
            f"meaning='{self.base.meanings}')>"
        )


class VerbRegularPerfectParticipleBase(Database, Searchable):
    __tablename__ = "verb_regular_perfect_participle_base"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_id = mapped_column(Integer, ForeignKey("base.id"), nullable=False)

    base: Mapped["Base"] = relationship(back_populates="verb_regular_perfect_participle_base", foreign_keys=[base_id])

    def __repr__(self):
        return (
            f"<VerbRegularPerfectParticipleBase(orth='{self.base.orth}', "
            f"meaning='{self.base.meanings}')>"
        )
    

class VerbIrregularPresentInfinitiveBase(Database, Searchable):
    __tablename__ = "verb_irregular_present_infinitive_base"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_id = mapped_column(Integer, ForeignKey("base.id"), nullable=False)

    base: Mapped["Base"] = relationship(back_populates="verb_irregular_present_infinitive_base", foreign_keys=[base_id])

    def __repr__(self):
        return (
            f"<VerbIrregularPresentInfinitiveBase(orth='{self.base.orth}', "
            f"meaning='{self.base.meanings}')>"
        )
    

class VerbIrregularPerfectParticipleBase(Database, Searchable):
    __tablename__ = "verb_irregular_perfect_participle_base"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    base_id = mapped_column(Integer, ForeignKey("base.id"), nullable=False)

    base: Mapped["Base"] = relationship(back_populates="verb_irregular_perfect_participle_base", foreign_keys=[base_id])

    def __repr__(self):
        return (
            f"<VerbIrregularPerfectParticipleBase(orth='{self.base.orth}', "
            f"meaning='{self.base.meanings}')>"
        )
