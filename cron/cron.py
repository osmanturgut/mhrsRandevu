import subprocess
import datetime
import time


def run_scheduled(start_time_str, end_time_str, kacSaniyedeBir=120, kacSaniyeCalissin=4):
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    while datetime.datetime.now() < start_time:
        time.sleep(1)
    while datetime.datetime.now() < end_time:
        try:
            process = subprocess.Popen(
                ["python3", "/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/requests/users.py"])
            time.sleep(kacSaniyeCalissin)

            if process.poll() is None:
                process.terminate()

        except Exception as e:
            print(f"Hata oluştu: {e}")

        time.sleep(kacSaniyedeBir)

if __name__ == "__main__":
    start_time_input = "2025-03-01 10:30:30"
    end_time_input = "2025-06-11 05:59:53"
    run_scheduled(start_time_input, end_time_input)
