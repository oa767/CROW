"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import os
import random
import pymongo as pm
from pymongo.server_api import ServerApi
import bson.json_util as bsutil

APP_HOME = os.environ["APP_HOME"]
TEST_MODE = os.environ.get("TEST_MODE", 0)
DB_DIR = f"{APP_HOME}/db"

if TEST_MODE:
    DB_DIR = "chatDB"
else:
    DB_DIR = "chatDB"

#field names in our DB:
ROOMS = "rooms"
USERS = "users"

USER_NM = "userName"
ROOM_NM = "roomName"
NUM_USERS = "num_users"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2

client = pm.MongoClient("mongodb+srv://oabouelnour:<cBhCCuTa3adSBKxc>@cluster0.52jag.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", server_api=ServerApi('1'))
print(client)


def fetch_all(collect_nm, key_nm):
    all_docs = {}
    for doc in client[DB_NAME][collect_nm].find():
        print(doc)
        all_docs[doc[key_nm]] = json.loads(bsutil.dumps(doc))
    return all_docs
    

def insert_doc(collect_nm, doc):
    client[DB_NAME][collect_nm].insert_one(doc)
    

def update_doc(collect_nm, doc):
    client[DB_NAME][collect_nm].update
    

def get_rooms():
    """
    A function to return a dictionary of all rooms.
    """
    return fetch_all(ROOMS, ROOM_NM)


def room_exists(roomname):
    rooms = get_rooms()
    return roomname in rooms


def add_room(roomname):
    """
    Add a room to the room database.
    """
    rooms = get_rooms()
    if rooms is None:
        return NOT_FOUND
    elif roomname in rooms:
        return DUPLICATE
    else:
        rooms[roomname] = {"num_users": 0, "users": []}
        insert_doc(ROOMS, {ROOM_NM: roomname, NUM_USERS: 0})
        return OK


def delete_room(roomname):
    if not room_exists(roomname):
        return NOT_FOUND
    return OK
    ###WORK IN PROGRESS###
    

def get_users():
    """
    A function to return a dictionary of all users.
    """
    return fetch_all(USERS, USER_NM)


def write_users(test):
    pass

def write_rooms(test):
    pass


def add_user(username):
    """
    This function adds a new user to the user db.
    """
    users = get_users()
    if users is None:
        return NOT_FOUND
    elif username in users:
        return DUPLICATE
    else:
        insert_doc(USERS, {USER_NM: username})
        return OK


def join_user(username):
    """
    Adds a user to a chat room.
    """
    rooms = get_rooms()
    if rooms is None:
        return NOT_FOUND
    else:
        random_room = random.choice(list(rooms))
        rooms[random_room]["users"].append(username)
        rooms[random_room]["num_users"] += 1
        write_rooms(rooms)
        return random_room
