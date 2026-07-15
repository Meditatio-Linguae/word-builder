import csv

from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from schemas.database import Database
from schemas.bases import Base as WordBase
from utils.search import CountryCode


def migrate(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
    Database.metadata.drop_all(engine, checkfirst=True)
    Database.metadata.create_all(engine, checkfirst=True)

    with Session(engine) as session:
        with open("data/bases.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                meanings = row[2]
                main_orth = row[0]
                other_orths = row[1].split("|") if row[1] != "" else []

                session.add(
                    WordBase(
                        orth=main_orth,
                        meanings=meanings
                    )
                )
                session.add_all(
                    [
                        WordBase(
                            orth=other_orth,
                            meanings=meanings
                        )
                        for other_orth in other_orths
                    ]
                )

        session.commit()
