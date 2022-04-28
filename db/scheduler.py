from schedule import every, repeat, run_pending
import time
import db.data as db
import db.db_connect as db_connect

@repeat(every(1).minute)
def test_scheduler():
    db.add_room("test_room")

@repeat(every(1).minute)
def test2_scheduler():
    try:
        db.delete_room("test_room")
    except:
        pass

@repeat(every(24).hours)
def auto_delete_rooms():
    lst = db.get_rooms()
    for room in lst:
        db.delete_room(room)

@repeat(every(24).hours)
def auto_delete_users():
    lst = db.get_users()
    for user in lst:
        db.delete_user(user)

while True:
    run_pending()
    time.sleep(1)