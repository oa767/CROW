"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api, fields, reqparse
import werkzeug.exceptions as wz
import db.data as db
import random

app = Flask(__name__)
CORS(app)
api = Api(app)

HELLO = 'Hello'
WORLD = 'World'


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    @api.response(HTTPStatus.OK, 'Success')
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO: WORLD}


@api.route('/users/list')
class ListUsers(Resource):
    """
    This endpoint returns a list of all users.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns a list of all users.
        """
        users = db.get_users()
        if users is None:
            raise (wz.NotFound("User db not found."))
        else:
            return users


@api.route('/rooms/<roomname>/id')
class RoomID(Resource):
    """
    This endpoint returns the ID for a specific room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, roomname):
        """
        Returns the room code for a specific room.
        """
        ID = db.get_room_code(roomname)
        if ID is None:
            raise (wz.NotFound(f"Room {roomname} not found."))
        else:
            return ID


@api.route('/users/list/<roomname>')
class ListUsersRoom(Resource):
    """
    This endpoint returns a list of all users from a specific room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, roomname):
        """
        Returns a list of all users for a specific room.
        """
        users = db.get_users_room(roomname)
        if users is None:
            raise (wz.NotFound(f"Chat room {roomname} not found."))
        else:
            return users


@api.route('/rooms/list')
class ListRooms(Resource):
    """
    This endpoint returns a list of all rooms.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Returns a list of all chat rooms.
        """
        rooms = db.get_rooms()
        if rooms is None:
            raise (wz.NotFound("Chat room db not found."))
        else:
            return rooms


@api.route('/rooms/create/<roomname>')
class CreateRoom(Resource):
    """
    This class supports adding a chat room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key has been found')
    def post(self, roomname):
        """
        This method adds a room to the room db.
        """
        ret = db.add_room(roomname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Chat room db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable(f"Chat room {roomname} already exists."))
        else:
            return f"{roomname} added."


@api.route('/users/create/<username>')
class CreateUser(Resource):
    """
    This class supports adding a user to the chat room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'A duplicate key has been found')
    def post(self, username):
        """
        This method adds a user to the users database.
        """
        ret = db.add_user(username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("User db not found."))
        elif ret == db.DUPLICATE:
            raise (wz.NotAcceptable(f"Username {username} already exists."))
        return f"{username} added."


@api.route('/rooms/delete/<roomname>')
class DeleteRoom(Resource):
    """
    This class enables deleting a chat room.
    While 'Forbidden` is a possible return value, we have not yet implemented
    a user privileges section, so it isn't used yet.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.FORBIDDEN,
                  'Only the owner of a room can delete it.')
    def post(self, roomname):
        """
        This method deletes a room from the room db.
        """
        ret = db.delete_room(roomname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound(f"Chat room {roomname} not found."))
        else:
            return f"{roomname} deleted."


@api.route('/users/delete/<username>')
class DeleteUser(Resource):
    """
    This class enables deleting a user from the database.
    While 'Forbidden` is a possible return value, we have not yet implemented
    a user privileges section, so it isn't used yet.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.FORBIDDEN,
                  'Only the user themselves can delete it.')
    def post(self, username):
        """
        This method deletes a user from the user db.
        """
        ret = db.delete_user(username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound(f"User {username} not found."))
        else:
            return f"{username} deleted."


@api.route('/rooms/join/random/<username>')
class JoinRandomRoom(Resource):
    """
    This class supports joining a random chat room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def post(self, username):
        """
        This method adds the user to a random chat room.
        """
        ret = db.join_random_room(username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("No chat rooms available."))
        else:
            return f"{username} has joined room {ret}."


@api.route('/rooms/join/preset/<username>')
class JoinPresetRoom(Resource):
    """
    This class supports joining a random chat room with a preset username.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def post(self, username):
        """
        This method adds a user with a preset username to a random chat room.
        """
        ret = db.join_preset_room(username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Something went wrong."))
        else:
            return f"{username} has joined room {ret}."


@api.route('/rooms/join/<roomcode>/<username>')
class JoinRoomCode(Resource):
    """
    This class supports joining a chat room using its room code.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'No room with this code exists')
    def post(self, roomcode, username):
        """
        This method adds the user to a chat room using its room code.
        """
        ret = db.join_room_code(roomcode, username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound(f"No chat rooms available"))
        elif ret == db.NOT_ACCEPTABLE:
            raise (wz.NotAcceptable(f"No chat room exists w/ ID {roomcode}."))
        else:
            return f"{username} has joined room {roomcode}."


interests_parser = reqparse.RequestParser()
interests_parser.add_argument('interests', action = 'split')


@api.route('/rooms/join/interests/<username>')
class JoinRoomInterests(Resource):
    """
    This class supports joining a chat room by matching with a user's specific interests.
    """
    @api.doc(parser = interests_parser)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def post(self, username):
        """
        This method adds the user to a chat room using its room code.
        """
        args = interests_parser.parse_args()
        interests = args["interests"]
        ret = db.join_room_interests(interests, username)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("No suitable chat room found. Please try joining a random room."))
        else:
            return {f"{username} has joined room {ret}.": f"{ret}"}


@api.route('/users/remove/<username>/<roomname>')
class RemoveUserFromRoom(Resource):
    """
    This class supports removing a user from a room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Only the user themselves or an admin can perform this operation.')
    def put(self, username, roomname):
        """
        This method removes a user from a room.
        """
        ret = db.remove_user_from_room(username, roomname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("User {username} cannot be found."))
        elif ret == db.NOT_ACCEPTABLE:
            raise (wz.NotFound("Only {username} or an admin can perform this operation."))
        else:
            return f"{username} has been removed from room {roomname}."


@api.route('/users/remove/<username>/<roomcode>')
class RemoveUserFromRoomID(Resource):
    """
    This class supports removing a user from a room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Only the user themselves or an admin can perform this operation.')
    def put(self, username, roomcode):
        """
        This method removes a user from a room.
        """
        ret = db.remove_user_from_room_id(username, roomcode)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("User {username} cannot be found."))
        elif ret == db.NOT_ACCEPTABLE:
            raise (wz.NotFound("Only {username} or an admin can perform this operation."))
        else:
            return f"{username} has been removed from room ID {roomcode}."


@api.route('/rooms/update/<roomname>/<newname>')
class UpdateRoom(Resource):
    """
    This class supports updating a chat room.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'You are not an authorized user.')
    def put(self, roomname, newname):
        """
        This method updates a room already in the room database.
        """
        ret = db.update_room(roomname, newname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("Chat room {roomname} cannot be found."))
        else:
            return f"{roomname} updated to {newname}."


@api.route('/users/update/<username>/<newname>')
class UpdateUser(Resource):
    """
    This class supports updating a user.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'You are not an authorized user.')
    def put(self, username, newname):
        """
        This method updates a user already in the user database.
        """
        ret = db.update_user(username, newname)
        if ret == db.NOT_FOUND:
            raise (wz.NotFound("User {username} cannot be found."))
        else:
            return f"{username} updated to {newname}."


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}
