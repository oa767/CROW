"""
This file holds the tests for endpoints.py.
"""

from unittest import TestCase, skip 
from flask_restx import Resource, Api
import random             

import API.endpoints as ep
import db.data as db

HUGE_NUM = 10000000000000

def new_entity_name(entity_name):
    int_name = random.randint(0, HUGE_NUM)
    return "new " + str(entity_name) + " - " + str(int_name)
    
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

    def test_create_user(self):
        """
        Checks to see if we can successfully create a new user.
        Post-condition 1: user is in DB.
        """
        cu = ep.CreateUser(Resource)
        new_user = new_entity_name("user")
        ret = cu.post(new_user)
        users = db.get_users_as_dict()
        self.assertIn(new_user, users)
        
    def test_create_room(self):
        """
        Checks to see if we can successfully create a new room.
        Post-condition 1: room is in DB.
        """
        cr = ep.CreateRoom(Resource)
        new_room = new_entity_name("room")
        ret = cr.post(new_room)
        rooms = db.get_rooms_as_dict()
        self.assertIn(new_room, rooms)
        
    def test_join_room(self):
        """
        Checks to see if a user can successfully join a room.
        Post-condition 1: user has joined room.
        """
        jr = ep.JoinRoom(Resource)
        ret = jr.post("test_username")
        rooms = db.get_rooms_as_dict()
        found = False
        for room in rooms:
            if "test_username" in rooms[room]["list_users"]:
                found = True
        self.assertTrue(found)

    def test_update_room(self):
        """
        Checks to see if a room can be updated.
        Post-condition 1: room has been updated.
        """
        cr = ep.CreateRoom(Resource)
        room = new_entity_name("room")
        ret = cr.post(room)
        ur = ep.UpdateRoom(Resource)
        ret = ur.put(room, "updatedname")
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
        cr = ep.CreateUser(Resource)
        user = new_entity_name("user")
        ret = cr.post(user)
        ur = ep.UpdateUser(Resource)
        ret = ur.put(user, "updatedname")
        users = db.get_users_as_dict()
        found = False
        for user in users:
            if "updatedname" == users[user]["user_name"]:
                found = True
        self.assertTrue(found)

    def test_list_rooms(self):
        """
        Post-condition 1: return is a list.
        """
        lr = ep.ListRooms(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, list)
