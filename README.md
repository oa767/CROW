
# Anonymous Chat Room
# Omar AbouelNour, Chino Guerrero, Randy Genere

## Main Function:

An anonymous chat room that deletes its history with a group of X people
(ideally 10 people).

## Main Features:

A website type application that can generate a chat room.
The user is placed in a random public chatroom.
Other users can be dropped into this public chat room.
Requires a code to enter a new chatroom.
Limited Slots (ideally 10 people).
Deletes after use (20 minutes after last message).

## Possible Features:

- File Sharing.
- Video Calls.
- GIFs.
- Screen Sharing.
- Whiteboard Mode.

## Requirements:

- Users are connected to a random public chat room as an anonymous user.
- Users can connect to different chat rooms using the code provided by each room.
- Rooms have limited user slots (ideally 10 slots).
- Chat history is deleted after the last message (20 minute grace period before deletion).
- Users can host a brand new private chat room for people who know the code for the room.

## Design:


- Option bars on the left hand side of the screen to view users in the current room which connects with the view_users endpoint.
- A button to 'create a private chat room' on the top-left of the API which connects with the create_room endpoint.
- Codes for room are displayed on the top of the screen/website which are randomly generated when a room is created.
- Chat interface in the center of screen.
- Users can choose their own private name.
- The same set of unique names will be used for each room.

