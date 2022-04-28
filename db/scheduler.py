from schedule import every, repeat, run_pending
import time

@repeat(every(24).hours)
def job():
    print("Testing")

while True:
    run_pending()
    time.sleep(1)