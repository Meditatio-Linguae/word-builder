from sqlalchemy import create_engine
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
import sys
from setups.migration import migrate
from setups.collection.verb import VerbCollectionBuilder
from setups.collection.adjective import AdjectiveCollectionBuilder
from setups.collection.noun import NounCollectionBuilder


config = dotenv_values(".env")

radicals_uri = config.get("RADICALS_URI")
engine = create_engine(radicals_uri, echo=True)

uri = config.get("SEARCH_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
search_db = client["word"]
word_compounds = search_db["test"]

arg1 = sys.argv[1]

if arg1 == "migrate":
    migrate(engine)
elif arg1 == "build":
    arg2 = sys.argv[2]
    collection_builder = None
    if arg2 == "verb":
        collection_builder = VerbCollectionBuilder()
        collection_builder.build(engine)
    elif arg2 == "adjective":
        collection_builder = AdjectiveCollectionBuilder()
        collection_builder.build(engine)
    elif arg2 == "noun":
        collection_builder = NounCollectionBuilder()
        collection_builder.build(engine)
    elif arg2 == "all":
        collection_builders = [VerbCollectionBuilder(), AdjectiveCollectionBuilder(), NounCollectionBuilder()]
        for builder in collection_builders:
            builder.build(engine)
    word_compounds.insert_many(collection_builder.compounded_words)
elif arg1 == "test-db-connection":
    client.admin.command("ping")
    print("Connected successfully")
elif arg1 == "drop-search":
    word_compounds.delete_many({})
        
client.close()