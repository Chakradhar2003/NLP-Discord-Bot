from pymongo import MongoClient

mongo_client=MongoClient("")
db = mongo_client['discord_db']
collection = db['toxicity_levels']

demo_doc={"user":"#1234","toxicity_level":2}
insert_doc=collection.insert_one(demo_doc)

mongo_client.close()