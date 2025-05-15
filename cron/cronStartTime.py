import time
import subprocess
from datetime import datetime
from pytz import timezone

def run_main():
    try:
        subprocess.run(
            ["python3", "/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/requests/users.py"],
            timeout=60
        )
    except subprocess.TimeoutExpired:
        print("users.py execution timed out.")

def run_scheduled(start_time_input, end_time_input):
    local_tz = timezone("Europe/Istanbul")
    start_time = local_tz.localize(datetime.strptime(start_time_input, "%Y-%m-%d %H:%M:%S"))
    end_time = local_tz.localize(datetime.strptime(end_time_input, "%Y-%m-%d %H:%M:%S"))

    while True:
        current_time = datetime.now(local_tz)
        print(f"Current Time: {current_time}, Start Time: {start_time}, End Time: {end_time}")

        if start_time <= current_time <= end_time:
            run_main()
        elif current_time > end_time:
            print("End time reached, stopping the process.")
            break
        time.sleep(1)


if __name__ == "__main__":
    start_time_input = "2025-02-19 09:59:35"
    end_time_input = "2025-02-19 10:03:20"
    run_scheduled(start_time_input, end_time_input)
