from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from .processing import get_pm

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_pm, 'interval', minutes=5)
    scheduler.start()