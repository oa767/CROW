"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import os
import random

APP_HOME = os.environ["APP_HOME"]
TEST_MODE = os.environ.get("TEST_MODE", 0)
DB_DIR = f"{APP_HOME}/db"

if TEST_MODE:
    DB_DIR = f"{APP_HOME}/db/test_dbs"
else:
    DB_DIR = f"{APP_HOME}/db"

ROOMS_DB = f"{APP_HOME}/db/rooms.json"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2


def write_rooms(rooms):
    """
    Write out the in-memory room list in proper DB format.
    """
    with open(ROOMS_DB, 'w') as f:
        json.dump(rooms, f, indent=4)


def get_rooms():
    """
    A function to return all chat rooms.
    """
    try:
        with open(ROOMS_DB) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        print("Rooms db not found.")
        return None


def add_room(roomname):
    """
    Add a room to the room database.
    Until we are using a real DB, we have a potential
    race condition here.
    """
    rooms = get_rooms()
    if rooms is None:
        return NOT_FOUND
    elif roomname in rooms:
        return DUPLICATE
    else:
        rooms[roomname] = {"num_users": 0, "users": []}
        write_rooms(rooms)
        return OK


def get_users():
    return {"John": {}}
    
    
def write_users():
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
        users[username] = {"num_users": 0}
        write_users(users)
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
