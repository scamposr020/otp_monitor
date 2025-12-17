import requests

def get_access_token(token_url, client_id, client_secret):
    response = requests.post(
        token_url,
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_email_otp(api_base_url, access_token, verification_id):
    url = f"{api_base_url}/v2.0/factors/emailotp/verifications/{verification_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def attempt_email_otp(api_base_url, access_token, verification_id, otp_code):
    url = f"{api_base_url}/v2.0/factors/emailotp/verifications/{verification_id}/attempt"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "otp": otp_code
    }

    response = requests.post(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

