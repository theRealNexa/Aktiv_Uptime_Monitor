import sqlite3

DB_FILE = "monitor.db"


def init_db():
    """Creates the checks table if it doesn't already exist.
    Call this once when the program starts."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status_code INTEGER,
            response_time_ms INTEGER,
            is_up INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_check(service_name, timestamp, status_code, response_time_ms, is_up):
    """Saves one check result as a new row.
    is_up should be True or False (SQLite stores it as 1 or 0)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO checks (service_name, timestamp, status_code, response_time_ms, is_up)
        VALUES (?, ?, ?, ?, ?)
    """, (service_name, timestamp, status_code, response_time_ms, int(is_up)))
    conn.commit()
    conn.close()


def get_recent_checks(service_name, limit=5):
    """Returns the most recent checks for a service, newest first.
    Used to check if we've failed enough times in a row to alert."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT is_up FROM checks
        WHERE service_name = ?
        ORDER BY id DESC
        LIMIT ?
    """, (service_name, limit))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]