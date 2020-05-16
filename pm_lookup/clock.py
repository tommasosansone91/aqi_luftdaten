
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from pm_lookup.processing.scheduled_processing import save_history_pm

sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    save_history_pm()
    print('This job is run every five minutes.')

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()