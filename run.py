import atexit
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
from app import app
scheduler = BackgroundScheduler()

def my_task():
    # Thêm code của bạn để chạy sau mỗi 30 phút vào đây
    import weather
    import apiservice
    import mergedata
    import training
    print("Scheduler is running...")


if __name__ == '__main__':
    scheduler.add_job(my_task, 'interval', minutes=2)
    scheduler.start()
    # Dừng scheduler khi tắt Flask app
    atexit.register(lambda: scheduler.shutdown(wait=False))
    app.run()









