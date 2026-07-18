import csv

from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from schemas.database import Database
from schemas.bases import Base as WordBase, NounBase


def migrate(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
    Database.metadata.drop_all(engine, checkfirst=True)
    Database.metadata.create_all(engine, checkfirst=True)

    with Session(engine) as session:
        with open("data/noun_bases.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                base = WordBase(
                    orth=row[1] if row[1] != "" else row[0],
                    meanings=row[4]
                )
                session.add(base)
                session.add(NounBase(declension=int(row[2]), base=base))

        session.commit()
