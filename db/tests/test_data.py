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
        Can we fetch user db?
        """
        users = db.get_users()
        self.assertIsInstance(users, list)

    def test_get_rooms(self):
        """
        Can we fetch user db?
        """
        rooms = db.get_rooms()
        self.assertIsInstance(rooms, list)

    def test_list_rooms(self):
        """
        Post-condition 1: return is a list.
        """
        lst = db.get_rooms()
        self.assertIsInstance(lst, list)