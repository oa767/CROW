"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip 
from flask_restx import Resource, Api

import API.endpoints as ep
import db.db as db

NEW_ROOM = "New room"

class EndpointTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_hello(self):
        hello = ep.HelloWorld(Resource)
        ret = hello.get()
        self.assertIsInstance(ret, dict)
        self.assertIn(ep.HELLO, ret)

    def test_create_room(self):
        """
        Post-condition 1: return is a dictionary.
        """
        cr = ep.CreateRoom(Resource)
        ret = cr.post(NEW_ROOM)
        lr = ep.ListRooms(Resource)
        rooms = db.get_rooms()
        self.assertIn(NEW_ROOM, rooms)
        
    def test_list_rooms1(self):
        """
        Post-condition 1: return is a dictionary.
        """
        lr = ep.ListRooms(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, dict)

    def test_list_rooms2(self):
        """
        Post-condition 2: keys to the dict are strings
        """
        lr = ep.ListRooms(Resource)
        ret = lr.get()
        for key in ret:
            self.assertIsInstance(key, str)

    def test_list_rooms3(self):
        """
        Post-condition 3: the values in the dict are themselves dicts
        """
        lr = ep.ListRooms(Resource)
        ret = lr.get()
        for val in ret.values():
            self.assertIsInstance(val, dict)
