import requests

def send_slack_notification(webhook_url, message):
    payload = {
        "text": message
    }

    response = requests.post(webhook_url, json=payload, timeout=10)
    response.raise_for_status()
