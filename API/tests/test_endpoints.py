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

    @skip("WORK IN PROGRESS!")
    def test_create_user(self):
        """
        Checks to see if we can successfully create a new user.
        Post-condition 1: user is in DB.
        """
        cu = ep.CreateUser(Resource)
        new_user = new_entity_name("user")
        ret = cu.post(new_user)
        users = db.get_users()
        self.assertIn(new_user, users)
        
    def test_create_room(self):
        """
        Checks to see if we can successfully create a new room.
        Post-condition 1: room is in DB.
        """
        cr = ep.CreateRoom(Resource)
        new_room = new_entity_name("room")
        ret = cr.post(new_room)
        #print(f'post {ret=}')
        rooms = db.get_rooms_as_dict()
        print("Create_Room:      ")
        print(f'{rooms=}')
        self.assertIn(new_room, rooms)
        
    def test_join_room(self):
        """
        Post-condition 1: return is a dictionary.
        """
        jr = ep.JoinRoom(Resource)
        ret = jr.post("test_username")
        rooms = db.get_rooms_as_dict()
        found = False
        for room in rooms:
            print(f'{rooms[room]=}')
            if "test_username" in rooms[room]["list_users"]:
                found = True
        self.assertTrue(found)
            
    def test_list_rooms1(self):
        """
        Post-condition 1: return is a list.
        """
        lr = ep.ListRooms(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, list)
