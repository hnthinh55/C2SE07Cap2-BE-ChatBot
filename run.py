import schedule
import subprocess
import time

def run_file(file_name):
    subprocess.run(["python", file_name])

# Hàm để đặt lịch chạy các file sau mỗi 30 phút
def schedule_files(file_list):
    for file_name in file_list:
        schedule.every(3).minutes.do(run_file, file_name)

# Thực thi file app.py
subprocess.run(["python", "app.py"])

# Đặt lịch chạy các file
file_list = ["importdata.py", "mergedata.py", "training.py"]
schedule_files(file_list)

# Vòng lặp để kiểm tra và thực thi các lịch chạy trong `schedule`
while True:
    schedule.run_pending()
    time.sleep(1)