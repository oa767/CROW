"""
This file holds the tests for db.py.
"""

from unittest import TestCase, skip
import random

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

class DBTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_users(self):
        """
        Post-condition 1: return is a list.
        """
        users = db.get_users()
        self.assertIsInstance(users, list)

    def test_get_rooms(self):
        """
        Post-condition 1: return is a list.
        """
        lst = db.get_rooms()
        self.assertIsInstance(lst, list)

    def test_get_rooms_as_dict(self):
        """
        Post-condition 1: return is a dictionary.
        """
        rooms = db.get_rooms_as_dict()
        self.assertIsInstance(rooms, dict)

    def test_get_users_as_dict(self):
        """
        Post-condition 1: return is a dictionary.
        """
        users = db.get_users_as_dict()
        self.assertIsInstance(users, dict)

    def test_get_room_code(self):
        """
        Post-condition 1: return is a string.
        """
        ID = db.get_room_code()
        self.assertIsInstance(ID, str)

    def test_get_users_room(self):
        """
        Post-condition 1: return is a list.
        """
        users = db.get_users_room()
        self.assertIsInstance(users, list)

    def test_add_room(self):
        """
        Checks to see if we can successfully create a new room.
        Post-condition 1: room is in DB.
        """
        new_room = new_entity_name("room")
        db.add_room(new_room)
        rooms = db.get_rooms_as_dict()
        self.assertIn(new_room, rooms)

    def test_add_user(self):
        """
        Checks to see if we can successfully create a new user.
        Post-condition 1: user is in DB.
        """
        new_user = new_entity_name("user")
        db.add_user(new_user)
        users = db.get_users_as_dict()
        self.assertIn(new_user, users)