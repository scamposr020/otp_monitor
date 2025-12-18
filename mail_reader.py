import imaplib
import email
import re
from datetime import datetime, timedelta


def read_otp_from_outlook(
    imap_server,
    email_user,
    email_password,
    wait_minutes=5
):
    """
    Connects to Outlook via IMAP and reads the latest OTP email.
    Returns the OTP code if found, otherwise None.
    """

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_password)
    mail.select("inbox")

    since_date = (
        datetime.utcnow() - timedelta(minutes=wait_minutes)
    ).strftime("%d-%b-%Y")

    status, messages = mail.search(
        None,
        f'(SINCE "{since_date}")'
    )

    if status != "OK":
        mail.logout()
        return None

    email_ids = messages[0].split()
    email_ids.reverse()  # newest first

    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject = msg.get("Subject", "")

        # Ajustar si conoces el subject exacto del OTP
        if "OTP" not in subject.upper():
            continue

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(
                        errors="ignore"
                    )
                    break
        else:
            body = msg.get_payload(decode=True).decode(
                errors="ignore"
            )

        # Buscar OTP (6 dígitos)
        match = re.search(r"\b\d{6}\b", body)
        if match:
            mail.logout()
            return match.group(0)

    mail.logout()
    return None

