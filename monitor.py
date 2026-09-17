import time
import requests
from datetime import datetime

from config import SERVICES, CHECK_INTERVAL_SECONDS, FAILURE_THRESHOLD, REQUEST_TIMEOUT_SECONDS
from db import init_db, save_check, get_recent_checks
from notifier import alert_service_down, alert_service_recovered


def check_service(url):
    """Pings one URL and returns (is_up, status_code, response_time_ms).
    is_up is False if the request fails or times out entirely."""
    try:
        start = time.time()
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        elapsed_ms = int((time.time() - start) * 1000)
        is_up = response.status_code < 500  # treat 5xx as down, everything else as up
        return is_up, response.status_code, elapsed_ms
    except requests.exceptions.RequestException:
        return False, None, None


def has_just_gone_down(service_name):
    """Returns True if the last FAILURE_THRESHOLD checks were all failures.
    Used so we only alert after repeated failures, not one blip."""
    recent = get_recent_checks(service_name, limit=FAILURE_THRESHOLD)
    if len(recent) < FAILURE_THRESHOLD:
        return False  # not enough history yet to be sure
    return all(status == 0 for status in recent)


def has_just_recovered(service_name):
    """Returns True if the most recent check is up, but the one before it was down.
    This is what tells us to send a 'recovered' message."""
    recent = get_recent_checks(service_name, limit=FAILURE_THRESHOLD + 1)
    if len(recent) < 2:
        return False
    latest_is_up = recent[0] == 1
    previous_were_down = all(status == 0 for status in recent[1:])
    return latest_is_up and previous_were_down


def run_one_check_cycle():
    """Checks every service once, saves results, and sends alerts if needed."""
    for service in SERVICES:
        name = service["name"]
        url = service["url"]

        is_up, status_code, response_time_ms = check_service(url)
        timestamp = datetime.now().isoformat()

        save_check(name, timestamp, status_code, response_time_ms, is_up)

        status_label = "UP" if is_up else "DOWN"
        print(f"[{timestamp}] {name}: {status_label} (status={status_code}, time={response_time_ms}ms)")

        if not is_up and has_just_gone_down(name):
            alert_service_down(name)
        elif is_up and has_just_recovered(name):
            alert_service_recovered(name)


def main():
    init_db()
    print("Uptime monitor started. Checking every", CHECK_INTERVAL_SECONDS, "seconds.")
    while True:
        run_one_check_cycle()
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()