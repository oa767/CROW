import pymongo as pm
import bson

client = pm.MongoClient()
print(client)

db = client["CROW_DB"]
print(db)
