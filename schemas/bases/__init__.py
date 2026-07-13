from sqlalchemy import (
    Integer,
    String
)
from sqlalchemy.orm import mapped_column
from schemas.database import Database
from utils.search import Searchable


class Base(Database, Searchable):
    __tablename__ = "base"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    orth = mapped_column(String(255), nullable=False)
    meanings = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"<Base(orth='{self.orth}', meaning='{self.meanings}')>"