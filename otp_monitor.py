import os
import time
from verify_api import (
    get_access_token,
    create_email_otp,
    attempt_email_otp
)
from mail_reader import read_otp_from_outlook
from slack_notifier import send_slack_notification


def main():
    token_url = os.getenv("VERIFY_TOKEN_URL")
    api_base_url = os.getenv("VERIFY_API_BASE_URL")
    client_id = os.getenv("VERIFY_CLIENT_ID")
    client_secret = os.getenv("VERIFY_CLIENT_SECRET")
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

    imap_server = os.getenv("OUTLOOK_IMAP_SERVER")
    email_user = os.getenv("OUTLOOK_EMAIL_USER")
    email_password = os.getenv("OUTLOOK_EMAIL_PASSWORD")

    try:
        # 1️⃣ Obtener access token
        access_token = get_access_token(
            token_url,
            client_id,
            client_secret
        )

        # 2️⃣ Crear verificación Email OTP
        verification_response = create_email_otp(
            api_base_url,
            access_token
        )

        verification_id = verification_response.get("id")

        if not verification_id:
            raise Exception(
                "Verification ID not returned by IBM Verify"
            )

        # 3️⃣ Esperar correo
        time.sleep(90)

        # 4️⃣ Leer inbox Outlook
        otp_code = read_otp_from_outlook(
            imap_server=imap_server,
            email_user=email_user,
            email_password=email_password
        )

        if not otp_code:
            send_slack_notification(
                slack_webhook,
                (
                    ":rotating_light: IBM Verify OTP Monitor FAILED\n\n"
                    "OTP email was not received."
                )
            )
            return

        # 5️⃣ Intentar validar OTP
        attempt_email_otp(
            api_base_url,
            access_token,
            verification_id,
            otp_code
        )

        # 6️⃣ Éxito
        send_slack_notification(
            slack_webhook,
            (
                ":white_check_mark: IBM Verify OTP Monitor OK\n\n"
                "OTP email received and validated successfully."
                )
        )

    except Exception as e:
        send_slack_notification(
            slack_webhook,
            (
                ":rotating_light: IBM Verify OTP Monitor ERROR\n\n"
                f"{str(e)}"
            )
        )
        raise


if __name__ == "__main__":
    main()
