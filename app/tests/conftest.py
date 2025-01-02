import pytest
import requests


@pytest.fixture(scope="session")
def get_auth_token():
    login_url = 'https://fo1.api.altius.finance/api/v0.0.2/login'

    login_payload = {
        "email": "fo1_test_user@whatever.com",
        "password": "Test123!"
    }

    response = requests.post(login_url, json=login_payload)

    assert response.status_code == 200, "Login failed, expected status code 200"

    response_data = response.json()

    assert "token" in response_data["success"], "The response does not contain a 'token' "

    token = response_data["success"]["token"]

    return token


@pytest.fixture(scope="session")
def post_comment_id(get_auth_token):
    post_url = "https://fo1.api.altius.finance/api/v0.0.3/deals/5644/comments"

    headers = {
        'Authorization': f"Bearer {get_auth_token}"
    }

    payload = {
        'audience': "tenants_team",
        'form_id': 5363,
        'question_id': 75339,
        'section_id': 16051,
        'text': "This is a comment"
    }

    response = requests.post(post_url, headers=headers, json=payload)
    response.raise_for_status()
    response_data = response.json()
    comment_id = response_data['data']['id']

    return comment_id
