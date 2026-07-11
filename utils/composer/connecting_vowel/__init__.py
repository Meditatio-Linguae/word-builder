from utils.search import Searchable


class ConnectingVowel(Searchable):
    def __init__(self, orth):
        self.orth = orth

    def to_searchable(self):
        return super().to_searchable(
            orth=self.orth,
            meanings="connecting vowel"
        )
    
    def __repr__(self):
        return f"<ConnectingVowel(orth='{self.relevant_orth()}')>"
