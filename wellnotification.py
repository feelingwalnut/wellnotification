#!/usr/bin/python3
import requests
import time
from datetime import datetime, timedelta

def check_log():
    response = requests.get("http://192.168.1.1/json.htm?type=command&param=getlightlog&idx=517")
    data = response.json()
    now = datetime.now()
    count = 0
    for entry in data['result']:
        timestamp = datetime.strptime(entry['Date'], '%Y-%m-%d %H:%M:%S')
        if now - timestamp < timedelta(days=1):
            count += 1
    return count

def send_notification(subject, body):
    requests.get(f"http://192.168.1.1/json.htm?type=command&param=sendnotification&subject={subject}&body={body}&subsystem=email")

def check_device_status():
    response = requests.get("http://192.168.1.1/json.htm?type=command&param=getdevices&rid=517")
    data = response.json()
    return data['result'][0]['Status']

def main():
    start_time = time.time()
    log_checked = False
    duration_notified = False
    while True:
        if not log_checked and check_log() > 4:
            send_notification('Well Pump Run Frequency', 'Pump was on more than four times today.')
            log_checked = True
        if check_device_status() == 'Off':
            break
        if not duration_notified and time.time() - start_time > 270:
            send_notification('Well Pump Run Duration', 'Pump has ran for more than 4.5 minutes.')
            duration_notified = True
            return
        time.sleep(10)

if __name__ == "__main__":
    main()
