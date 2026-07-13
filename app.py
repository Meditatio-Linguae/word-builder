from sqlalchemy import create_engine
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
import sys
from setups.collection import CollectionBuilder
from setups.migration import migrate


config = dotenv_values(".env")

radicals_uri = config.get("RADICALS_URI")
db_engine = create_engine(radicals_uri, echo=True)

uri = config.get("SEARCH_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
search_db = client["word"]
search_engine = search_db["test"]

arg1 = sys.argv[1]

if arg1 == "migrate":
    migrate(db_engine)
elif arg1 == "build":
    collection_builder = CollectionBuilder(db_engine, search_engine)
    collection_builder.generate()
elif arg1 == "test-db-connection":
    client.admin.command("ping")
    print("Connected successfully")
elif arg1 == "drop-search":
    search_engine.delete_many({})
        
client.close()