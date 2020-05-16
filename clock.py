
from apscheduler.schedulers.blocking import BlockingScheduler

from pm_lookup.processing.scheduled_processing import save_history_pm

sched = BlockingScheduler()

sched.add_job(save_history_pm, 'cron', id='run_every_1_min', minute='*/1')


sched.start()


# -------------


# @sched.scheduled_job('interval', minutes=1)
# def timed_job():
#     save_history_pm()
#     print('This job is run every five minutes.')

# # @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# # def scheduled_job():
# #     print('This job is run every weekday at 5pm.')

# sched.start()