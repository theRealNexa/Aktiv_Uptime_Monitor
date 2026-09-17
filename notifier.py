import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text):
    """Sends a message to your Telegram chat via the bot.
    Returns True if it sent successfully, False otherwise."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")
        return False


def alert_service_down(service_name):
    send_telegram_message(f"🔴 ALERT: {service_name} appears to be DOWN.")


def alert_service_recovered(service_name):
    send_telegram_message(f"🟢 RECOVERED: {service_name} is back up.")