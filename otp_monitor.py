import os
import time
from verify_api import (
    get_access_token,
    create_email_otp,
    attempt_email_otp
)
from slack_notifier import send_slack_notification


def main():
    token_url = os.getenv("VERIFY_TOKEN_URL")
    api_base_url = os.getenv("VERIFY_API_BASE_URL")
    client_id = os.getenv("VERIFY_CLIENT_ID")
    client_secret = os.getenv("VERIFY_CLIENT_SECRET")
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
    verification_id = os.getenv("VERIFY_EMAIL_OTP_VERIFICATION_ID")

    try:
        # 1️⃣ Obtener token
        access_token = get_access_token(
            token_url,
            client_id,
            client_secret
        )

        # 2️⃣ Disparar OTP
        create_email_otp(api_base_url, access_token, verification_id)

        # 3️⃣ Esperar correo
        time.sleep(90)

        # 4️⃣ Leer inbox (pendiente)
        otp_code = None

        if not otp_code:
            send_slack_notification(
                slack_webhook,
                ":rotating_light: IBM Verify OTP Monitor FAILED\n\nOTP email was not received."
            )
            return

        # 5️⃣ Validar OTP
        attempt_email_otp(
            api_base_url,
            access_token,
            verification_id,
            otp_code
        )

        # 6️⃣ Éxito
        send_slack_notification(
            slack_webhook,
            ":white_check_mark: IBM Verify OTP Monitor OK\n\nOTP email received and validated."
        )

    except Exception as e:
        send_slack_notification(
            slack_webhook,
            f":rotating_light: IBM Verify OTP Monitor ERROR\n\n{str(e)}"
        )
        raise


if __name__ == "__main__":
    main()

