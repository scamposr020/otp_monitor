import requests


def get_access_token(token_url, client_id, client_secret):
    payload = {
        "grant_type": "client_credentials",
        "scope": "openid",
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(
        token_url,
        data=payload,
        headers=headers,
        timeout=10
    )
    response.raise_for_status()

    return response.json()["access_token"]


def create_email_otp(api_base_url, access_token):
    """
    Creates an Email OTP verification and returns the verification response
    (including verification_id)
    """
    url = f"{api_base_url}/v2.0/factors/emailotp/verifications"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, timeout=10)
    response.raise_for_status()

    return response.json()


def attempt_email_otp(api_base_url, access_token, verification_id
