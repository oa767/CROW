"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip 
from flask_restx import Resource, Api
import random             

import API.endpoints as ep
import db.data as db
import db.db_connect as db_connect

# field names in our DB:
ROOMS = "rooms"
USERS = "users"
USER_NM = "user_name"
ROOM_NM = "room_name"
NUM_USERS = "num_users"
USERS_LIST = "list_users"
ID = "_id"

HUGE_NUM = 10000000000000

def new_entity_name(entity_name):
    int_name = random.randint(0, HUGE_NUM)
    return "new " + str(entity_name) + " - " + str(int_name)
    
class EndpointTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_list_rooms(self):
        """
        Post-condition 1: return is a list.
        """
        endpoint = ep.ListRooms(Resource)
        ret = endpoint.get()
        self.assertIsInstance(ret, list)

    def test_update_room(self):
        """
        Checks to see if a room can be updated.
        Post-condition 1: room has been updated.
        """
        room = new_entity_name("room")
        db.add_room(room)
        rooms = db.get_rooms_as_dict()
        if self.assertIn(room, rooms):
            db.update_room(room, "updatedname")
            rooms = db.get_rooms_as_dict()
            found = False
            for room in rooms:
                if "updatedname" == rooms[room]["room_name"]:
                    found = True
            self.assertTrue(found)

    def test_update_user(self):
        """
        Checks to see if a user can be updated.
        Post-condition 1: user has been updated.
        """
        user = new_entity_name("user")
        db.add_user(user)
        users = db.get_users_as_dict()
        if self.assertIn(user, users):
            db.update_user(user, "updatedname")
            users = db.get_users_as_dict()
            found = False
            for user in users:
                if "updatedname" == users[user]["user_name"]:
                    found = True
            self.assertTrue(found)

    def test_delete_room(self):
        """
        Checks to see if we can successfully delete a room.
        Post-condition 1: room is not in DB.
        """
        room = new_entity_name("room")
        db.add_room(room)
        if self.assertTrue(db.room_exists(room)):
            db.delete_room(room)
            self.assertFalse(db.room_exists(room))

    def test_delete_user(self):
        """
        Checks to see if we can successfully delete a user.
        Post-condition 1: user is not in DB.
        """
        user = new_entity_name("user")
        db.add_user(user)
        if self.assertTrue(db.user_exists(user)):
            db.delete_user(user)
            self.assertFalse(db.user_exists(user))

    def test_remove_user_room(self):
        """
        Checks to see if we can successfully remove a user from a chat room.
        Post-condition 1: user is not in room.
        """
        user = new_entity_name("user")
        joined_room = db.join_random_room(user)
        room_list = db.get_users_room(joined_room)
        if self.assertIn(user, room_list):
            db.remove_user_room(user, joined_room)
            self.assertNotIn(user, room_list)

    def test_remove_user_room(self):
        """
        Checks to see if we can successfully remove a user from a chat room.
        Post-condition 1: user is not in room.
        """
        user = new_entity_name("user")
        joined_room = db.join_random_room(user)
        room_list = db.get_users_room(joined_room)
        if self.assertIn(user, room_list):
            db.remove_user_room(user, joined_room)
            self.assertNotIn(user, room_list)

    def test_join_random_room(self):
        """
        Checks to see if a user can successfully join a room.
        Post-condition 1: user has joined room.
        """
        db.join_random_room("test_username")
        rooms = db.get_rooms_as_dict()
        found = False
        for room in rooms:
            if "test_username" in rooms[room]["list_users"]:
                found = True
        self.assertTrue(found)

    def test_join_room_code(self):
        """
        Checks to see if a user can successfully join a room using a specific roomcode.
        Post-condition 1: user has joined room.
        """
        ob_id = "620f1e5f16a2e3f23e0de44e"
        db.join_room_code(ob_id, "test_username")
        rooms = db_connect.fetch_all_as_dict(ROOMS, ID)
        found = False
        if "test_username" in rooms[db_connect.create_object_id(ob_id)]["list_users"]:
            found = True
        self.assertTrue(found)

    def test_join_preset_room(self):
        """
        Checks to see if a user can successfully join a room.
        Post-condition 1: user has joined room.
        """
        db.join_preset_room("Raven")
        rooms = db.get_rooms_as_dict()
        found = False
        for room in rooms:
            if "Raven" in rooms[room]["list_users"]:
                found = True
        self.assertTrue(found)

    def test_join_room_interests(self):
        """
        Checks to see if a user can successfully join a room using a specific set of interests.
        Post-condition 1: user has joined room.
        """
        interests = ["Reading"]
        db.join_room_interests(interests, "test_username")
        rooms = db_connect.fetch_all_as_dict(ROOMS, ROOM_NM)
        found = False
        if "test_username" in rooms["Software Engineering"]["list_users"]:
            found = True
        self.assertTrue(found)
