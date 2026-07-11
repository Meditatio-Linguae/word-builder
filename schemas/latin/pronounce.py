from enum import Enum
from sqlalchemy import (
    Integer,
    Enum as SQLEnum,
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


class PronominalCategory(Enum):
    INDEFINITIVE = "indefinitive"
    PERSONAL = "personal"
    INTERROGATIVE = "interrogative"


# class PronounceStem(Base, Searchable):
#     __tablename__ = "pronounce_stem"

#     id = mapped_column(Integer, primary_key=True, autoincrement=True)
#     orth = mapped_column(String(255), nullable=False)
#     category = mapped_column(SQLEnum(PronominalCategory, name="pronominal_category"), nullable=True)
#     radical_id = mapped_column(Integer, ForeignKey("radical.id"), nullable=False)

#     radical: Mapped["Radical"] = relationship(back_populates="pronounce_stem", foreign_keys=[radical_id])

#     def __repr__(self):
#         return (
#             f"<PronounceStem(orth='{self.radical.orth}', "
#             f"origin_of_tongue='{self.radical.origin_of_tongue}', "
#             f"meaning='{self.radical.meanings}')>"
#         )