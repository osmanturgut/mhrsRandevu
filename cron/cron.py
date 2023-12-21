import subprocess
import datetime
import time

def run_scheduled(start_time_str, end_time_str, interval_seconds=90, run_duration_seconds=4):
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    while datetime.datetime.now() < start_time:
        time.sleep(1)

    while datetime.datetime.now() < end_time:
        process = subprocess.Popen(["python3", "/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/requests/myUserRequests.py"])

        time.sleep(run_duration_seconds)

        if process.poll() is not None:
            break
        process.terminate()
        time.sleep(interval_seconds)

if __name__ == "__main__":
    # Başlangıç ve bitiş tarihlerini manuel olarak ayarlayın
    start_time_input = "2023-12-17 13:53:00"
    end_time_input = "2023-12-17 20:00:10"

    run_scheduled(start_time_input, end_time_input)
