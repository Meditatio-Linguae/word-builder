from sqlalchemy import (
    Integer,
    ForeignKey,
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base import Base
from utils.search import Searchable


class AdverbStem(Base, Searchable):
    __tablename__ = "adverb_stem"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="adverb_stem", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<AdverbStem(orth='{self.radical.orth}'), "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}'>"
        )