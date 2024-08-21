import subprocess
import datetime
import time

def run_scheduled(start_time_str, end_time_str, kacSaniyedeBir=360, kacSaniyeCalissin=4):
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

    while datetime.datetime.now() < start_time:
        time.sleep(1)

    while datetime.datetime.now() < end_time:
        process = subprocess.Popen(["python3", "/Users/btcyz155/Desktop/projects/kisisel/mhrsRandevu/requests/test.py"])

        time.sleep(kacSaniyeCalissin)

        if process.poll() is not None:
            break
        process.terminate()
        time.sleep(kacSaniyedeBir)

if __name__ == "__main__":
    # Başlangıç ve bitiş tarihlerini manuel olarak ayarlayın
    start_time_input = "2024-08-09 15:48:47"
    end_time_input = "2024-09-09 07:40:00"

    run_scheduled(start_time_input, end_time_input)
