from abc import (
    ABC,
    abstractmethod
)
from wordfreq import zipf_frequency
from nltk.corpus import wordnet as wn


class CollectionBuilder(ABC):
    def __init__(self):
        self.compounded_words = []

    def _validate_syntax(self, orth):
        pass
    
    def _validate_semantics(self, orth):
        # TODO
        # return zipf_frequency(orth, "en") > 0
        return bool(wn.synsets(orth))
    
    def _special_case(self, orth):
        pass

    def _collect(self, parts):
        orth = ("".join([part.relevant_orth() for part in parts]))
        if self._validate_semantics(orth):
            self.compounded_words.append({
                orth: {
                    "parts": [part.to_searchable() for part in parts]
                }
            })

    @abstractmethod
    def _build(self, stems, suffixes, **prefixes):
        pass

    @abstractmethod
    def build(self, engine):
        pass
