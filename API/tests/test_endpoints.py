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

    def test_hello(self):
        hello = ep.HelloWorld(Resource)
        ret = hello.get()
        self.assertIsInstance(ret, dict)
        self.assertIn(ep.HELLO, ret)
    
    def test_list_rooms(self):
        """
        Post-condition 1: return is a list.
        """
        lr = ep.ListRooms(Resource)
        ret = lr.get()
        self.assertIsInstance(ret, list)

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

    def test_join_random_room(self):
        """
        Checks to see if a user can successfully join a room.
        Post-condition 1: user has joined room.
        """
        jr = ep.JoinRandomRoom(Resource)
        ret = jr.post("test_username")
        rooms = db.get_rooms_as_dict()
        found = False
        for room in rooms:
            if "test_username" in rooms[room]["list_users"]:
                print(rooms[room]["_id"])
                print(type(rooms[room]["_id"]))
                found = True
        self.assertTrue(found)
        
    def test_join_room_code(self):
        """
        Checks to see if a user can successfully join a room using a specific roomcode.
        Post-condition 1: user has joined room.
        """
        jr = ep.JoinRoomCode(Resource)
        ob_id = "620f1e5f16a2e3f23e0de44e"
        ret = jr.post(ob_id, "test_username")
        rooms = db_connect.fetch_all_as_dict(ROOMS, ID)
        found = False
        if "test_username" in rooms[db_connect.create_object_id(ob_id)]["list_users"]:
            found = True
        self.assertTrue(found)

def test_join_room_interests(self):
        """
        Checks to see if a user can successfully join a room using a specific set of interests.
        Post-condition 1: user has joined room.
        """
        jr = ep.JoinRoomInterests(Resource)
        interests = ["Reading"]
        ret = jr.post(interests, "test_username")
        rooms = db_connect.fetch_all_as_dict(ROOMS, ROOM_NM)
        found = False
        if "test_username" in rooms["Software Engineering"]["list_users"]:
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
        rooms = db.get_rooms_as_dict()
        if self.assertIn(room, rooms):
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
        users = db.get_users_as_dict()
        if self.assertIn(user, user):
            ur = ep.UpdateUser(Resource)
            ret = ur.put(user, "updatedname")
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
        cr = ep.CreateRoom(Resource)
        room = new_entity_name("room")
        ret = cr.post(room)
        if self.assertTrue(db.room_exists(room)):
            dr = ep.DeleteRoom(Resource)
            ret = dr.post(room)
            self.assertFalse(db.room_exists(room))

    def test_delete_user(self):
        """
        Checks to see if we can successfully delete a user.
        Post-condition 1: user is not in DB.
        """
        cr = ep.CreateUser(Resource)
        user = new_entity_name("user")
        ret = cr.post(user)
        if self.assertTrue(db.user_exists(user)):
            du = ep.DeleteUser(Resource)
            ret = du.post(user)
            self.assertFalse(db.user_exists(user))
