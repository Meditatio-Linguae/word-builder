from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.latin.adjective import AdjectivePositiveStem
from schemas.latin.noun import NounStem, NounSuffix
from schemas.latin.preposition import Preposition
from setups.collection import CollectionBuilder
from utils.composer import compose_word


class NounCollectionBuilder(CollectionBuilder):
    def _build(self, stems, suffixes, **prefixes):
        adj_pos_stems = prefixes.get("adj_pos_stems")
        prepositions = prefixes.get("prepositions")

        for stem in stems:
            self._collect([stem])
            for preposition in prepositions:
                for preposition_noun_combination in compose_word(preposition, stem):
                    self._collect(preposition_noun_combination)
            for first_suffix in suffixes:
                for noun_suffix_combination in compose_word(stem, first_suffix):
                    self._collect(noun_suffix_combination)
                    for second_suffix in suffixes:
                        if noun_suffix_combination[0].orth == "circ" and noun_suffix_combination[1].orth == "ule" and second_suffix.orth == "ate":
                            print(noun_suffix_combination, second_suffix)
                            exit()
                        for first_suffix_and_second_suffix_combination in compose_word(noun_suffix_combination[-1], second_suffix):
                            print(first_suffix_and_second_suffix_combination)
                            self._collect(noun_suffix_combination[:-1] + first_suffix_and_second_suffix_combination)
                    for preposition in prepositions:
                        for preposition_noun_combination in compose_word(preposition, noun_suffix_combination[0]):
                            self._collect(preposition_noun_combination + noun_suffix_combination[1:])
                    for adj_pos_stem in adj_pos_stems:
                        for adj_pos_verb_combination in compose_word(adj_pos_stem, noun_suffix_combination[0]):
                            self._collect(adj_pos_verb_combination + noun_suffix_combination[1:])
            
    def build(self, engine):
        with Session(engine) as session:
            prepositions = session.scalars(select(Preposition)).all()
            adj_pos_stems = session.scalars(select(AdjectivePositiveStem)).all()
            noun_suffixes = session.scalars(select(NounSuffix)).all()
            noun_stems = session.scalars(select(NounStem)).all()

            self._build( 
                noun_stems, 
                noun_suffixes, 
                adj_pos_stems=adj_pos_stems,
                prepositions=prepositions
            )
