from dataclasses import dataclass
from enum import Enum

@dataclass
class Attribute:
    orth: str
    meanings: str


class CountryCode(Enum):
    LA = "la"
    EL = "el"
    EN = "en"
    FR = "fr"


class Searchable(Attribute):
    def to_searchable(self):
        return {
            "orth": self.orth,
            "meanings": self.meanings,
        }
