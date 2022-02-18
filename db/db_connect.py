"""
This file contains some common MongoDB code.
"""
import os
import pymongo as pm
import json
import bson.json_util as bsutil


# all of these will eventually be put in the env:
user_nm = "oabouelnour"
cloud_svc = "cluster0.52jag.mongodb.net"
passwd = os.environ.get("MONGO_PASSWD", '')
cloud_mdb = "mongodb+srv"
db_params = "retryWrites=true&w=majority"
db_nm = "chatDB"
test_db = "testDB"

client = None
test = True

if test:
    database_name = test_db
else:
    database_name = db_nm


def get_client():
    """
    This provides a uniform way to get the client across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    """
    global client
    if test:
        print("Connecting to testDB.")
        client = pm.MongoClient(f"mongodb+srv://oabouelnour:{passwd}@"
                                + f"{cloud_svc}/{test_db}?"
                                + db_params)
    else:
        print("Connecting to chatDB.")
        client = pm.MongoClient(f"mongodb+srv://oabouelnour:{passwd}@"
                                + f"{cloud_svc}/{db_nm}?"
                                + db_params)
    return client


def fetch_doc(collect_nm, filters = {}):
    """
    Fetch one record that meets filters.
    """
    return client[database_name][collect_nm].find_one(filters)


def delete_doc(collect_nm, filters = {}):
    """
    Deletes doc from collection.
    """
    return client[database_name][collect_nm].delete_one(filters)


def fetch_all(collect_nm, key_nm):
    all_docs = []
    for doc in client[database_name][collect_nm].find():
        # print(doc)
        all_docs.append(json.loads(bsutil.dumps(doc)))
    return all_docs


def fetch_all_as_dict(collect_nm, key_nm):
    all_docs = []
    for doc in client[database_name][collect_nm].find():
        all_docs.append(doc)
    all_dict = {}
    for doc in all_docs:
        # print(f'{doc=}')
        all_dict[doc[key_nm]] = doc
    return all_dict


def insert_doc(collect_nm, doc):
    """
    Inserts doc into collection.
    """
    client[database_name][collect_nm].insert_one(doc)


def update_doc(collect_nm, filters = {}, update_string = {}):
    """
    Inserts doc into collection.
    """
    client[database_name][collect_nm].update_one(filters, update_string)
