import atexit
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
from app import app
import time
scheduler = BackgroundScheduler()
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask_socketio import SocketIO, emit
def my_task():
    # Thêm code của bạn để chạy sau mỗi 30 phút vào đây
  
    subprocess.run("python weather.py", shell=True)
    subprocess.run("python apiservice.py", shell=True)
    subprocess.run("python mergedata.py", shell=True)
    subprocess.run("python training.py", shell=True)
    print("Scheduler is running...")
class FileChangedHandler(FileSystemEventHandler):
    def __init__(self):
        self.updated = False
        self.updating =False
        super().__init__()
    def on_modified(self, event):
        if event.src_path.endswith('data.json'):
            print('data.json is modified')
            if self.updating:
                self.updating = False
                print('data.json saved')
                print('Stopping Flask API...')
                subprocess.Popen('taskkill /f /fi "imagename eq app.py"', shell=True)
                time.sleep(10)
                print('Starting Flask API...')
                subprocess.Popen('python app.py', shell= True)
                print('"python app.py"')
            else:
                self.updating = True
                print('data.json updating')
    def on_closed(self, event):
        if event.src_path.endswith('data.json') and self.updating:
            self.updating =False
            print('Stopping Flask API...')
            subprocess.Popen('taskkill /f /fi "imagename eq python.exe"', shell=True)
            time.sleep(1)
            print('Starting Flask API...')
            subprocess.Popen('python app.py', shell=True)
            print('"python app.py"')
def start_observer():
    observer = Observer()
    observer.schedule(FileChangedHandler(), path='E:\Chatbot-app\C2SE07Cap2-BE-ChatBot\\', recursive=True)
    observer.start()

    # Chạy observer trong khi Flask Server đang chạy
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
socket = SocketIO(app)
if __name__ == '__main__':
    scheduler.add_job(my_task, 'interval', minutes=2)
    scheduler.start()
    # Dừng scheduler khi tắt Flask app
    atexit.register(lambda: scheduler.shutdown(wait=False))
    observer = Observer()
    observer.schedule(FileChangedHandler(), path='D:\ThinhProject\C2SE07Cap2-BE-ChatBot\\', recursive=True)
    observer.start()
    socket.run(app,debug= True)

    observer.stop()
    observer.join()









