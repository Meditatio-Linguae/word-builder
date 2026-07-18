from schemas.bases import NounBase
from schemas.suffixes import Suffix
from schemas.suffixes.noun_to_adjective import NounToAdjectiveSuffix
from utils.composer import ComposingRule
from utils.misc import clone_runtime_object


class Ile(NounToAdjectiveSuffix):
    def __init__(self):
        self.orth = "ile"
        self.meanings = "pertaining to"


class Il(NounToAdjectiveSuffix):
    def __init__(self):
        self.orth = "il"
        self.meanings = "pertaining to"
