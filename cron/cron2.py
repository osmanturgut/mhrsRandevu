import subprocess
import datetime
import time

def run_scheduled(start_time_str, end_time_str, kacSaniyedeBir=6, kacSaniyeCalissin=4):
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    while datetime.datetime.now() < start_time:
        time.sleep(1)

    while datetime.datetime.now() < end_time:
        process = subprocess.Popen(["python3", "/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/requests/users2.py"])

        time.sleep(kacSaniyeCalissin)

        if process.poll() is not None:
            break
        process.terminate()
        time.sleep(kacSaniyedeBir)

if __name__ == "__main__":
    start_time_input = "2024-12-01 00:32:52"
    end_time_input = "2025-12-01 09:50:40"

    run_scheduled(start_time_input, end_time_input)
