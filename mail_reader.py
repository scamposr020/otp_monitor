import imaplib
import email
import os
import time


def wait_for_otp_email(timeout_seconds=180, poll_interval=10):
    mail = imaplib.IMAP4_SSL(os.environ["OUTLOOK_IMAP_SERVER"])
    mail.login(
        os.environ["OUTLOOK_EMAIL_USER"],
        os.environ["OUTLOOK_EMAIL_PASSWORD"],
    )

    end_time = time.time() + timeout_seconds

    while time.time() < end_time:
        mail.select("inbox")
        status, messages = mail.search(None, '(UNSEEN)')

        if status != "OK":
            time.sleep(poll_interval)
            continue

        for eid in messages[0].split()[::-1]:
            _, msg_data = mail.fetch(eid, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            subject = msg.get("Subject", "").lower()
            if "otp" in subject or "verification" in subject:
                mail.logout()
                return True

        time.sleep(poll_interval)

    mail.logout()
    return False
