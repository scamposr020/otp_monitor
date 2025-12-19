import sys
import os
import requests
from verify_api import get_access_token, trigger_email_otp
from mail_reader import wait_for_otp_email


def send_slack(message):
    requests.post(
        os.environ["SLACK_WEBHOOK_URL"],
        json={"text": message},
        timeout=10,
    )


def main():
    try:
        token = get_access_token()

        # This triggers the Email OTP
        trigger_email_otp(token)

        # Now we only validate email delivery
        email_received = wait_for_otp_email()

        if email_received:
            send_slack(
                ":white_check_mark: IBM Verify OTP Monitor OK\n"
                "Email OTP was successfully received."
            )
        else:
            send_slack(
                ":x: IBM Verify OTP Monitor FAILED\n"
                "Email OTP was NOT received."
            )
            sys.exit(1)

    except Exception as e:
        send_slack(
            f":rotating_light: IBM Verify OTP Monitor ERROR\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
