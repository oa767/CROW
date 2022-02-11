"""
This file holds the tests for db.py.
"""

from unittest import TestCase, skip
# import random

import db.data as db

FAKE_USER = "Fake user"


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