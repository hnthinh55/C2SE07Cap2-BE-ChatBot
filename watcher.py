import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Tìm quá trình Flask app đang chạy
class FileChangedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"{event.src_path} has been modified")
        subprocess.call(["python", "app.py"])
if __name__ == "__main__":
    event_handler = FileChangedHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(180)  # Wait for an hour
    except KeyboardInterrupt:
        observer.stop()
    observer.join()