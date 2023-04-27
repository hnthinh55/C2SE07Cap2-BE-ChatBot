import os
import subprocess
import psutil

# Tìm quá trình Flask app đang chạy
flask_pid = None
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if proc.info['cmdline'] is not None and \
       len(proc.info['cmdline']) > 1 and \
       'flask' in proc.info['cmdline'][1]:
        flask_pid = proc.info['pid']
        break
if flask_pid is None:
    print("Không tìm thấy quá trình Flask app đang chạy.")
    exit()

# Tắt Flask app
try:
    os.kill(flask_pid, 9)
    os.waitpid(flask_pid, 0)
    print("Đã tắt Flask app.")
except OSError:
    print("Không thể tắt Flask app.")

# Khởi động lại Flask app
from app import app
if __name__ == "__main__":
        app.run()
print("Đã khởi động lại Flask app.")