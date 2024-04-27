import time
import subprocess
from datetime import datetime, time as dtime, timedelta
def run_main():
    subprocess.run(["python3", "/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/requests/myUserRequests.py"])
def run_scheduled():
    start_time = dtime(hour=00, minute=27)
    end_time = dtime(hour=10, minute=2)
    #interval = timedelta(seconds=0)  # 10 saniyelik aralık
    while True:
        current_time = datetime.now().time()
        if start_time <= current_time <= end_time:
            run_main()
        #time_until_next_run = datetime.combine(datetime.today(), start_time) + timedelta(days=1) - datetime.now()
        #time.sleep(min(interval.total_seconds(), time_until_next_run.total_seconds()))
if __name__ == "__main__":
    run_scheduled()