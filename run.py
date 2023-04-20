import schedule
import time

def run_file():
    import weather
    import apiservice
    import mergedata
    import training
    pass
from app import app
if __name__ == "__main__":
    app.run()
schedule.every(5).minutes.do(run_file)

while True:
    schedule.run_pending()
    time.sleep(1)











