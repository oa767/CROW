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

ROOMS_DB = f"{APP_HOME}/db/rooms.json"
if TEST_MODE:
    ROOMS_DB = f"{DB_DIR}/test_rooms.json"
else:
    ROOMS_DB = f"{DB_DIR}/rooms.json"

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
