from sqlalchemy import (
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base import Base
from utils.search import Searchable


class Preposition(Base, Searchable):
    __tablename__ = "preposition"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

    radical: Mapped["Radical"] = relationship(back_populates="preposition", foreign_keys=[radical_id])

    def __repr__(self):
        return (
            f"<Prefix(orth='{self.relevant_orth()}'), "
            f"origin_of_tongue='{self.radical.origin_of_tongue}', "
            f"meaning='{self.radical.meanings}'>"
        )