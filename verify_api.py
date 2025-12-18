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


def create_email_otp_verification(access_token, email):
    base_url = os.environ["VERIFY_API_BASE_URL"]
    url = f"{base_url}/v2.0/factors/emailotp/verifications"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "email": email
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(
            f"Create Email OTP failed: {response.status_code} - {response.text}"
        )

    return response.json()["id"]
