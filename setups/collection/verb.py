from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas.latin.adjective import AdjectivePositiveStem
from schemas.latin.adverb import AdverbStem
from schemas.latin.noun import NounStem
from schemas.latin.preposition import Preposition
from schemas.latin.verb import (
    VerbAssimilatedRadicalStem, 
    VerbAssimilatedRadicalSuffix, 
    VerbIrregularPerfectParticipleStem, 
    VerbIrregularPresentInfinitiveStem, 
    VerbPerfectParticipleSuffix, 
    VerbPresentInfinitiveSuffix, 
    VerbRegularPerfectParticipleStem, 
    VerbRegularPresentInfinitiveStem
)
from setups.collection import CollectionBuilder
from utils.composer import compose_word


class VerbCollectionBuilder(CollectionBuilder):
    def _build(self, stems, suffixes, **prefixes):
        noun_stems = prefixes.get("noun_stems")
        adj_pos_stems = prefixes.get("adj_pos_stems")
        adverb_stems = prefixes.get("adverb_stems")
        prepositions = prefixes.get("prepositions")

        for stem in stems:
            self._collect([stem])
            for preposition in prepositions:
                for preposition_verb_combination in compose_word(preposition, stem):
                    self._collect(preposition_verb_combination)
            for suffix in suffixes:
                for verb_suffix_combination in compose_word(stem, suffix):
                    self._collect(verb_suffix_combination)
                    for preposition in prepositions:
                        for preposition_verb_combination in compose_word(preposition, verb_suffix_combination[0]):
                            self._collect(preposition_verb_combination + verb_suffix_combination[1:])
                    for noun_stem in noun_stems:
                        for noun_verb_combination in compose_word(noun_stem, verb_suffix_combination[0]):
                            self._collect(noun_verb_combination + verb_suffix_combination[1:])
                    for adj_pos_stem in adj_pos_stems:
                        for adj_pos_verb_combination in compose_word(adj_pos_stem, verb_suffix_combination[0]):
                            self._collect(adj_pos_verb_combination + verb_suffix_combination[1:])
                    for adverb_stem in adverb_stems:
                        for adverb_verb_combination in compose_word(adverb_stem, verb_suffix_combination[0]):
                            self._collect(adverb_verb_combination + verb_suffix_combination[1:])

    def build(self, engine):
        with Session(engine) as session:
            prepositions = session.scalars(select(Preposition)).all()
            noun_stems = session.scalars(select(NounStem)).all()
            adj_pos_stems = session.scalars(select(AdjectivePositiveStem)).all()
            adverb_stems = session.scalars(select(AdverbStem)).all()

            # verb_assimilated_radical_suffixes = session.scalars(select(VerbAssimilatedRadicalSuffix)).all()
            # verb_assimilated_radical_stems = session.scalars(select(VerbAssimilatedRadicalStem))).all()
            # self._build(
            #     prefixes, 
            #     verb_assimilated_radical_stems, 
            #     verb_assimilated_radical_suffixes, 
            #     noun_stems=noun_stems, 
            #     adj_pos_stems=adj_pos_stems, 
            #     adverb_stems=adverb_stems
            # )
            
            # verb_present_infinitive_suffixes = session.scalars(select(VerbPresentInfinitiveSuffix)).all()
            # verb_regular_present_infinitive_stems = session.scalars(select(VerbRegularPresentInfinitiveStem)).all()
            # self._build(
            #     prefixes, 
            #     verb_regular_present_infinitive_stems, 
            #     verb_present_infinitive_suffixes, 
            #     noun_stems=noun_stems, 
            #     adj_pos_stems=adj_pos_stems, 
            #     adverb_stems=adverb_stems
            # )
            # verb_irregular_present_infinitive_stems = session.scalars(select(VerbIrregularPresentInfinitiveStem)).all()
            # self._build(
            #     prefixes, 
            #     verb_irregular_present_infinitive_stems, 
            #     verb_present_infinitive_suffixes, 
            #     noun_stems=noun_stems, 
            #     adj_pos_stems=adj_pos_stems, 
            #     adverb_stems=adverb_stems
            # )

            verb_perfect_participle_suffixes = session.scalars(select(VerbPerfectParticipleSuffix)).all()
            verb_regular_perfect_participle_stems = session.scalars(select(VerbRegularPerfectParticipleStem)).all()
            # self._build(
            #     prefixes, 
            #     verb_regular_perfect_participle_stems, 
            #     verb_perfect_participle_suffixes, 
            #     noun_stems=noun_stems, 
            #     adj_pos_stems=adj_pos_stems, 
            #     adverb_stems=adverb_stems
            # )
            # verb_irregular_perfect_participle_stems = session.scalars(select(VerbIrregularPerfectParticipleStem)).all()
            # self._build(
            #     prefixes, 
            #     verb_irregular_perfect_participle_stems, 
            #     verb_perfect_participle_suffixes, 
            #     noun_stems=noun_stems, 
            #     adj_pos_stems=adj_pos_stems, 
            #     adverb_stems=adverb_stems
            # )