# https://github.com/dbader/schedule
# http://www.reddit.com/r/Python/comments/1f6s7s/schedule_python_job_scheduling_for_humans/

import schedule
from time import sleep

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    sleep(1)

# related: http://pythonhosted.org/APScheduler/
