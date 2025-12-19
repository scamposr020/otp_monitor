import os
import requests


def get_access_token():
    token_url = os.environ["VERIFY_TOKEN_URL"]

    payload = {
        "grant_type": "client_credentials",
        "client_id": os.environ["VERIFY_CLIENT_ID"],
        "client_secret": os.environ["VERIFY_CLIENT_SECRET"],
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"Token request failed: {response.status_code} - {response.text}"
        )

    return response.json()["access_token"]


def trigger_email_otp(access_token):
    """
    This function intentionally stops at MFA challenge.
    The login attempt itself triggers the Email OTP.
    """

    url = f"{os.environ['VERIFY_API_BASE_URL']}/v1.0/authentication"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "username": os.environ["VERIFY_MONITOR_USERNAME"],
        "password": os.environ["VERIFY_MONITOR_PASSWORD"],
    }

    response = requests.post(url, json=payload, headers=headers)

    # Expected behavior:
    # 401 / 403 / challenge-required → OTP already sent
    if response.status_code in (401, 403):
        return True

    # Any 2xx would be unexpected but acceptable
    if response.status_code in (200, 201):
        return True

    raise Exception(
        f"Authentication trigger failed: {response.status_code} - {response.text}"
    )
