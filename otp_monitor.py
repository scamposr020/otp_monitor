import os
import sys
from verify_api import get_access_token, create_email_otp_verification
from mail_reader import wait_for_otp_email
import requests


def send_slack_notification(message, success=True):
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]

    payload = {
        "text": message
    }

    requests.post(webhook_url, json=payload)


def main():
    try:
        access_token = get_access_token()

        otp_email = os.environ["OUTLOOK_EMAIL_USER"]
        create_email_otp_verification(access_token, otp_email)

        email_received = wait_for_otp_email()

        if email_received:
            send_slack_notification(
                ":white_check_mark: IBM Verify OTP Monitor OK\nOTP email received successfully."
            )
        else:
            send_slack_notification(
                ":x: IBM Verify OTP Monitor FAILED\nOTP email was NOT received.",
                success=False
            )
            sys.exit(1)

    except Exception as e:
        send_slack_notification(
            f":rotating_light: IBM Verify OTP Monitor ERROR\n{str(e)}",
            success=False
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
