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
    def relevant_orth(self):
        if hasattr(self, "orth") and self.orth is not None:
            return self.orth
        else:
            return self.base.orth
        
    def relevant_meanings(self):
        if hasattr(self, "meanings") and self.orth is not None:
            return self.meanings
        else:
            return self.base.meanings
        
    def to_searchable(self):
        return {
            "orth": self.relevant_orth(),
            "meanings": self.relevant_meanings(),
        }
