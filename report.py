import sqlite3
from datetime import datetime, timedelta

from config import SERVICES

DB_FILE = "monitor.db"


def get_stats(service_name, since_hours):
    """Returns (total_checks, up_checks, avg_response_time_ms) for a service
    over the last `since_hours` hours."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cutoff = (datetime.now() - timedelta(hours=since_hours)).isoformat()

    cursor.execute("""
        SELECT is_up, response_time_ms FROM checks
        WHERE service_name = ? AND timestamp >= ?
    """, (service_name, cutoff))
    rows = cursor.fetchall()
    conn.close()

    total = len(rows)
    if total == 0:
        return 0, 0, None

    up_count = sum(1 for is_up, _ in rows if is_up == 1)
    response_times = [rt for _, rt in rows if rt is not None]
    avg_response = sum(response_times) / len(response_times) if response_times else None

    return total, up_count, avg_response


def print_report():
    print("=" * 50)
    print("UPTIME REPORT")
    print("=" * 50)

    for service in SERVICES:
        name = service["name"]
        print(f"\n{name}")
        print("-" * len(name))

        for label, hours in [("Last 24h", 24), ("Last 7d", 24 * 7)]:
            total, up_count, avg_response = get_stats(name, hours)
            if total == 0:
                print(f"  {label}: no data yet")
                continue

            uptime_pct = (up_count / total) * 100
            avg_str = f"{avg_response:.0f}ms" if avg_response else "N/A"
            print(f"  {label}: {uptime_pct:.1f}% uptime ({up_count}/{total} checks) | avg response: {avg_str}")


if __name__ == "__main__":
    print_report()