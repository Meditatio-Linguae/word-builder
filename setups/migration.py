import csv

from sqlalchemy import (
    MetaData,
    select
)
from sqlalchemy.orm import Session

from schemas.latin.adjective import AdjectiveClassNo, AdjectiveComparativeStem, AdjectiveNumeralStem, AdjectivePositiveStem, AdjectiveSuffix, AdjectiveSuperlativeStem, Degree
from schemas.latin.adverb import AdverbStem
from schemas.latin.base import Base
from schemas.latin.noun import NounClassNo, NounStem, NounSuffix
from schemas.latin.preposition import Preposition
from schemas.latin.radical import CountryCode, Radical
from schemas.latin.verb import VerbAssimilatedRadicalStem, VerbAssimilatedRadicalSuffix, VerbClassNo, VerbIrregularPerfectParticipleStem, VerbIrregularPresentInfinitiveStem, VerbPerfectParticipleSuffix, VerbPresentInfinitiveSuffix, VerbRegularPerfectParticipleStem, VerbRegularPresentInfinitiveStem


def migrate(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine, checkfirst=True)

    with Session(engine) as session:
        with open("data/verb_regular_stems.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                origin_of_tongue = CountryCode(row[7])
                meanings = row[6]
                is_deponent = True if row[5] == "TRUE" else False
                is_istem = True if row[4] == "TRUE" else False
                conjugation_no = VerbClassNo(row[3])
                radical_orth = row[2]
                assimilated_radical_orth = row[1] if row[1] != "" else radical_orth
                principal_parts = row[0].split("|")

                radical = Radical(
                    orth=radical_orth, 
                    meanings=meanings,
                    origin_of_tongue=origin_of_tongue
                )
                session.add(radical)
                session.add(
                    VerbAssimilatedRadicalStem(
                        orth=assimilated_radical_orth,
                        radical=radical
                    )
                )
                session.add_all([
                    VerbRegularPresentInfinitiveStem(
                        orth=principal_part_orth,
                        conjugation_no=conjugation_no,
                        is_istem=is_istem,
                        is_deponent=is_deponent,
                        radical=radical
                    ) if i == 0 else
                    VerbRegularPerfectParticipleStem(
                        orth=principal_part_orth,
                        conjugation_no=conjugation_no,
                        is_istem=is_istem,
                        is_deponent=is_deponent,
                        radical=radical
                    )
                    for i, principal_part_orth in enumerate(principal_parts) if principal_part_orth != "-"
                ])

        with open("data/verb_irregular_stems.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                origin_of_tongue = CountryCode(row[3])
                meanings = row[2]
                radical_orth = row[1]
                principal_parts = row[0].split("|")

                radical = Radical(
                    orth=radical_orth, 
                    meanings=meanings,
                    origin_of_tongue=origin_of_tongue
                )
                session.add(radical)
                session.add(
                    VerbAssimilatedRadicalStem(
                        orth=radical_orth,
                        radical=radical
                    )
                )
                session.add_all([
                    VerbIrregularPresentInfinitiveStem(
                        orth=principal_part_orth,
                        radical=radical
                    ) if i == 0 else
                    VerbIrregularPerfectParticipleStem(
                        orth=principal_part_orth,
                        radical=radical
                    )
                    for i, principal_part_orth in enumerate(principal_parts) if principal_part_orth != "-"
                ])
                                
        with open("data/verb_suffixes.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                radical = Radical(
                    orth=row[1], 
                    meanings=row[6],
                    origin_of_tongue=CountryCode(row[7])
                )
                session.add(radical)
                radical_required = True if row[2] == "TRUE" else False
                pai_required = True if row[3] == "TRUE" else False
                ppp_required = True if row[4] == "TRUE" else False
                # converted_pos = PartOfSpeech(row[5])
                assimilated_orths = row[0].split("|")

                if pai_required:
                    session.add_all(
                        [
                            VerbPresentInfinitiveSuffix(
                                orth=orth,
                                # converted_pos=converted_pos,
                                radical=radical
                            )
                            for orth in assimilated_orths
                        ]
                    )
                
                if ppp_required:
                    session.add_all(
                        [
                            VerbPerfectParticipleSuffix(
                                orth=orth,
                                # converted_pos=converted_pos,
                                radical=radical
                            )
                            for orth in assimilated_orths
                        ]
                    )
                
                if radical_required:
                    session.add_all(
                        [
                            VerbAssimilatedRadicalSuffix(
                                orth=orth,
                                # converted_pos=converted_pos,
                                radical=radical
                            )
                            for orth in assimilated_orths
                        ]
                    )

        with open("data/adjective_stems.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                origin_of_tongue = CountryCode(row[5])
                meanings = row[4]
                degree = Degree(row[3])
                radical_orth = row[0]
                orth = row[1] if row[1] != "" else radical_orth

                radical = Radical(
                    orth=radical_orth, 
                    meanings=meanings,
                    origin_of_tongue=origin_of_tongue
                )
                session.add(radical)

                if degree == Degree.POSITIVE:
                    declension_no = AdjectiveClassNo(row[2])
                    session.add(
                        AdjectivePositiveStem(
                            orth=orth,
                            declension_no=declension_no,
                            radical=radical
                        )
                    )
                elif degree == Degree.COMPARATIVE:
                    session.add(
                        AdjectiveComparativeStem(
                            orth=orth,
                            radical=radical
                        )
                    )
                elif degree == Degree.SUPERLATIVE:
                    session.add(
                        AdjectiveSuperlativeStem(
                            orth=orth,
                            radical=radical
                        )
                    )
                elif degree == Degree.NUMERAL:
                    session.add(
                        AdjectiveNumeralStem(
                            orth=orth,
                            radical=radical
                        )
                    )

        with open("data/adjective_suffixes.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                assimilated_orths = row[0].split("|")

                radical = Radical(
                    orth=row[1], 
                    meanings=row[3],
                    origin_of_tongue=CountryCode(row[4])
                )
                session.add(radical)
                session.add_all(
                    [
                        AdjectiveSuffix(
                            orth=orth,
                            # converted_pos=PartOfSpeech(row[2]),
                            radical=radical
                        )
                        for orth in assimilated_orths
                    ]
                )

        with open("data/noun_stems.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                root_orth = row[0]
                radical = Radical(
                    orth=root_orth, 
                    meanings=row[4],
                    origin_of_tongue=CountryCode(row[5])
                )
                session.add(radical)
                session.add(
                    NounStem(
                        orth=row[1] if row[1] != "" else root_orth,
                        declension_no=NounClassNo(row[2]),
                        radical=radical
                    )
                )
            
        with open("data/noun_suffixes.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                radical_orth = row[0]
                radical = Radical(
                    orth=radical_orth, 
                    meanings=row[4],
                    origin_of_tongue=CountryCode(row[5])
                )
                session.add(radical)

                declensions_required = row[2]
                if declensions_required != "*":
                    declension_nos = declensions_required.split(", ")
                    noun_suffixes = []
                    for declension_no in declension_nos:
                        noun_suffixes.append(
                            NounSuffix(
                                orth=radical_orth,
                                # converted_pos=PartOfSpeech(row[3]),
                                declension_required=NounClassNo(declension_no),
                                radical=radical
                            )
                        )
                    session.add_all(noun_suffixes)
                else:
                    session.add(
                        NounSuffix(
                            orth=radical_orth,
                            # converted_pos=PartOfSpeech(row[3]),
                            radical=radical
                        )
                    )

        with open("data/prepositions.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                root_orth = row[0]
                orth = row[1] if row[1] != "" else root_orth
                radical = Radical(
                    orth=root_orth, 
                    meanings=row[2],
                    origin_of_tongue=CountryCode(row[3])
                )
                session.add(radical)
                session.add(
                    Preposition(
                        orth=orth,
                        radical=radical
                    )
                )

        with open("data/adverb_stems.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                radical = Radical(
                    orth=row[0], 
                    meanings=row[1],
                    origin_of_tongue=CountryCode(row[2])
                )
                session.add(radical)
                session.add(
                    AdverbStem(
                        orth=row[0],
                        radical=radical
                    )
                )

        session.commit()
