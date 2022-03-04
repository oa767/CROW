"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import os
import random
import db.db_connect as db

APP_HOME = os.environ["APP_HOME"]

# field names in our DB:
ROOMS = "rooms"
USERS = "users"

USER_NM = "user_name"
ROOM_NM = "room_name"
NUM_USERS = "num_users"
USERS_LIST = "list_users"
ID = "_id"

OK = 0
NOT_FOUND = 1
DUPLICATE = 2

client = db.get_client()
print(client)


def get_rooms():
    """
    A function to return a list of all rooms.
    """
    return db.fetch_all(ROOMS, ROOM_NM)


def get_rooms_as_dict():
    """
    A function to return a dictionary of all rooms.
    """
    return db.fetch_all_as_dict(ROOMS, ROOM_NM)


def get_users():
    """
    A function to return a list of all users.
    """
    return db.fetch_all(USERS, USER_NM)


def get_users_as_dict():
    """
    A function to return a dictionary of all users.
    """
    return db.fetch_all_as_dict(USERS, USER_NM)


def room_exists(roomname):
    """
    See if a room with roomname is in the db.
    Returns True of False.
    """
    rec = db.fetch_one(ROOMS, {ROOM_NM: roomname})
    return rec is not None


def user_exists(username):
    """
    See if a user with username is in the db.
    Returns True of False.
    """
    rec = db.fetch_one(USERS, filters={USER_NM: username})
    return rec is not None


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
        db.insert_doc(ROOMS, {ROOM_NM: roomname, NUM_USERS: 0, USERS_LIST: []})
        return OK


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
        db.insert_doc(USERS, {USER_NM: username})
        return OK


def delete_room(roomname):
    """
    Deletes a room from the room database.
    """
    if not room_exists(roomname):
        return NOT_FOUND
    else:
        db.delete_doc(ROOMS, {ROOM_NM: roomname})
        return OK


def delete_user(username):
    """
    Deletes a user from the user database.
    """
    if not user_exists(username):
        return NOT_FOUND
    else:
        db.delete_doc(USERS, {USER_NM: username})
        return OK


def join_random_room(username):
    """
    Adds a user to a chat room.
    """
    rooms = get_rooms_as_dict()
    if rooms is None:
        return NOT_FOUND
    else:
        random_room = random.choice(list(rooms))
        lst = rooms[random_room][USERS_LIST]
        num = rooms[random_room][NUM_USERS]
        ob_id = rooms[random_room][ID]
        lst.append(username)
        num += 1
        db.update_doc(ROOMS, {ID : ob_id}, { "$set" : {USERS_LIST: lst, NUM_USERS: num}})
        return rooms[random_room][ROOM_NM]


def join_room_code(roomcode, username):
    """
    Adds a user to a chat room.
    """
    rooms = db.fetch_all_as_dict(ROOMS, ID)
    if rooms is None:
        return NOT_FOUND
    else:
        try:
            requested_room = rooms[roomcode]
            lst = rooms[roomcode][USERS_LIST]
            num = rooms[roomcode][NUM_USERS]
            lst.append(username)
            num += 1
            db.update_doc(ROOMS, {ID : roomcode}, { "$set" : {USERS_LIST: lst, NUM_USERS: num}})
        except KeyError:
            return NOT_FOUND


def update_room(roomname, newname):
    """
    Updates a room in the room database.
    """
    rooms = get_rooms_as_dict()
    found = False
    if rooms is None:
        return NOT_FOUND
    else:
        for room in rooms:
            if rooms[room][ROOM_NM] == roomname:
                ob_id = rooms[room][ID]
                found = True
        if not found:
            return NOT_FOUND
        else:
            db.update_doc(ROOMS, {ID : ob_id}, { "$set" : {ROOM_NM: newname}})
            return rooms[roomname][ROOM_NM]


def update_user(username, newname):
    """
    Updates a user in the user database.
    """
    users = get_users_as_dict()
    found = False
    if users is None:
        return NOT_FOUND
    else:
        for user in users:
            if users[user][USER_NM] == username:
                ob_id = users[user][ID]
                found = True
        if not found:
            return NOT_FOUND
        else:
            db.update_doc(USERS, {ID : ob_id}, { "$set" : {USER_NM: newname}})
            return users[username][USER_NM]
