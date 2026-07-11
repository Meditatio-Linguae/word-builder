from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.latin.adjective import (
    AdjectiveComparativeStem, 
    AdjectiveNumeralStem, 
    AdjectivePositiveStem, 
    AdjectiveSuffix, 
    AdjectiveSuperlativeStem
)
from schemas.latin.preposition import Preposition
from setups.collection import CollectionBuilder
from utils.composer import compose_word


class AdjectiveCollectionBuilder(CollectionBuilder):
    def _build(self, stems, suffixes, **prefixes):
        prepositions = prefixes.get("preposition")
        for stem in stems:
            self._collect([stem])
            for preposition in prepositions:
                for preposition_adjective_combination in compose_word(preposition, stem):
                    self._collect(preposition_adjective_combination)
            for suffix in suffixes:
                for adjective_suffix_combination in compose_word(stem, suffix):
                    self._collect(adjective_suffix_combination)
                    for preposition in prepositions:
                        for preposition_adjective_combination in compose_word(preposition, adjective_suffix_combination[0]):
                            self._collect(preposition_adjective_combination + adjective_suffix_combination[1:])

    def build(self, engine):
        with Session(engine) as session:
            prefixes = session.scalars(select(Preposition)).all()
            adj_suffixes = session.scalars(select(AdjectiveSuffix)).all()
            
            adj_pos_stems = session.scalars(select(AdjectivePositiveStem)).all()
            self._build(prefixes, adj_pos_stems, adj_suffixes)
            
            # adj_comp_stems = session.scalars(select(AdjectiveComparativeStem).join(AdjectiveComparativeStem.radical)).all()
            # self._build(prefixes, adj_comp_stems, adj_suffixes)
            
            # adj_sup_stems = session.scalars(select(AdjectiveSuperlativeStem).join(AdjectiveSuperlativeStem.radical)).all()
            # self._build(prefixes, adj_sup_stems, adj_suffixes)
            
            # adj_num_stems = session.scalars(select(AdjectiveNumeralStem).join(AdjectiveNumeralStem.radical)).all()
            # self._build(prefixes, adj_num_stems, adj_suffixes)
