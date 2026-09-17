# Aktiv - Uptime Monitor

A lightweight Python service that monitors the uptime of deployed web apps and sends real-time Telegram alerts when something goes down — or comes back up.

## Why I built this

I have a couple of projects deployed on free-tier hosting (Render, Netlify), and free-tier backends like Render's tend to spin down after periods of inactivity. Rather than finding out my app was down when a recruiter or user clicked the link, I built a small monitor that pings my services on an interval, logs the results, and pings me on Telegram the moment something changes state.

It's intentionally general-purpose — it doesn't know or care what it's watching, so it works for any URL, not just my own projects.

## How it works

- `monitor.py` runs a loop that checks every configured service every few minutes
- Each check result (status code, response time, up/down) is saved to a local SQLite database (`monitor.db`)
- Alerts are only sent on **state changes** — going down, or recovering — not on every single check, to avoid spamming
- A service is only marked "down" after a configurable number of consecutive failures, to avoid false alarms from a single dropped request
- `report.py` reads the database and prints uptime percentage and average response time over the last 24 hours and 7 days

## Project structure

```
uptime-monitor/
├── monitor.py           # main check loop
├── db.py                 # SQLite storage layer
├── notifier.py            # Telegram alert logic
├── config.py               # service list, thresholds, intervals
├── secrets.example.py       # template for Telegram credentials
├── report.py                 # CLI uptime report
└── generate_status.py          # writes STATUS.md from current data
```

## Setup

1. Clone the repo and create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Mac/Linux
   pip install requests
   ```

2. Copy `secrets.example.py` to `secrets.py` and fill in your own Telegram bot token and chat ID:
   - Create a bot via [@BotFather](https://t.me/BotFather) on Telegram to get a token
   - Message [@userinfobot](https://t.me/userinfobot) to get your numeric chat ID

3. Edit `config.py` to list the services you want to monitor.

4. Run the monitor:
   ```
   python monitor.py
   ```

5. Check a report any time:
   ```
   python report.py
   ```

## Example alert

```
🔴 ALERT: Xentient Backend appears to be DOWN.
...
🟢 RECOVERED: Xentient Backend is back up.
```

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.
