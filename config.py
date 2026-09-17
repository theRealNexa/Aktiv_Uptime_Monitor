# List every service you want to watch here.
# "name" is just a label for your reports/alerts.
# "url" must be a full URL, including https://
SERVICES = [
    {"name": "Xentient Backend", "url": "https://xentient-backend.onrender.com"},
    {"name": "Xentient Frontend", "url": "https://xentient.netlify.app"},
]

# How often to check all services, in seconds.
# 300 = every 5 minutes. Don't go too low or you'll hammer free-tier services.
CHECK_INTERVAL_SECONDS = 300

# How many consecutive failures before we consider a service "really" down
# and send an alert. This avoids false alarms from one dropped request.
FAILURE_THRESHOLD = 2

# How many seconds to wait for a response before treating it as a timeout.
REQUEST_TIMEOUT_SECONDS = 10

# Telegram bot credentials for sending alerts.
# TOKEN comes from @BotFather. CHAT_ID is your personal numeric ID from @userinfobot.
# Real values live in secrets.py, which is gitignored and never pushed to GitHub.
from secrets import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID