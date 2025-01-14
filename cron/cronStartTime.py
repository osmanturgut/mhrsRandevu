import time
import subprocess
from datetime import datetime

def run_main():
    subprocess.run(["python3", "/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/requests/users2.py"])

def run_scheduled():
    start_time_input = "2025-01-10 14:59:50"
    end_time_input = "2025-05-05 10:01:30"

    start_time = datetime.strptime(start_time_input, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time_input, "%Y-%m-%d %H:%M:%S")

    while True:
        current_time = datetime.now()
        if start_time <= current_time <= end_time:
            run_main()
            #time.sleep(1)  # Her çalıştırmadan sonra 1 saniye bekle
        elif current_time > end_time:
            print("End time reached, stopping the process.")
            break
        time.sleep(1)
if __name__ == "__main__":
    run_scheduled()