import subprocess
import datetime
import time

def run_scheduled(start_time_str, end_time_str, interval_seconds=8, run_duration_seconds=1):
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    while datetime.datetime.now() < start_time:
        time.sleep(1)

    while datetime.datetime.now() < end_time:
        process = subprocess.Popen(["python", "myUserRequests.py"])

        time.sleep(run_duration_seconds)

        if process.poll() is not None:
            break
        process.terminate()
        time.sleep(interval_seconds)

if __name__ == "__main__":
    # Başlangıç ve bitiş tarihlerini manuel olarak ayarlayın
    start_time_input = "2023-12-17 00:53:25"
    end_time_input = "2023-12-17 00:54:10"

    run_scheduled(start_time_input, end_time_input)
