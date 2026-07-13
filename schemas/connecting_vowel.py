from utils.search import Searchable


class ConnectingVowel(Searchable):
    def __init__(self, orth):
        self.orth = orth
        self.meanings = "connecting vowel"
        self.origin_of_tongue = None
