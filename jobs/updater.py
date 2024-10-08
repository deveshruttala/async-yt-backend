from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedulee

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(schedulee, 'interval', seconds = 10) # adding the job and running it every 10 seconds periodically
	scheduler.start()