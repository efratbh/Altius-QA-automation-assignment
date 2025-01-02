import requests
import time

login_url = 'https://fo1.api.altius.finance/api/v0.0.2/login'
deals_list_url = 'https://fo1.api.altius.finance/api/v0.0.2/deals-list'

# Login Tests

def test_successful_login():
    # Verify login is successful with valid, registered credentials

    valid_payload = {
        "email": "fo1_test_user@whatever.com",
        "password": "Test123!"
    }

    response = requests.post(login_url, json=valid_payload)
    response_data = response.json()

    assert response.status_code == 200, f"Login failed: expected status code 200, got {response.status_code}. Response: {response_data}"
    assert "success" in response_data, f"Login response missing 'success' key. Response: {response_data}"
    assert "token" in response_data["success"], "Token not found in the 'success' response."


def test_empty_credentials():
    # Test to verify login fails when both email and password are empty

    invalid_email_payload = {
        "email": "",
        "password": ""
    }

    response = requests.post(login_url, json=invalid_email_payload)
    response_data = response.json()

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}. Response: {response_data}"
    assert response_data["status"] == "error", f"Expected error status, got {response_data['status']}. Response: {response_data}"
    assert response_data["errors"]["login"][0] == "The email and password combination cannot be authenticated", \
        f"Unexpected error message: {response_data['errors']['login'][0]}"


def test_unregistered_valid_email_with_existing_password():
    # Test valid email format but not registered, with an existing password

    invalid_email_payload = {
        "email": "test@userwhatever",
        "password": "Test123!"
    }

    response = requests.post(login_url, json=invalid_email_payload)
    response_data = response.json()

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}. Response: {response_data}"
    assert response_data["status"] == "error", f"Expected error status, got {response_data['status']}. Response: {response_data}"
    assert response_data["errors"]["login"][0] == "The login credentials provided are incorrect. If you forgot your password, use the link below to recover it.", \
        f"Unexpected error message: {response_data['errors']['login'][0]}"


def test_invalid_email_format():
    # Test to verify login fails with invalid email format

    invalid_email_payload = {
        "email": "testuserwhatever.com",
        "password": "Test123!"
    }

    response = requests.post(login_url, json=invalid_email_payload)
    response_data = response.json()

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}. Response: {response_data}"
    assert response_data["status"] == "error", f"Expected error status, got {response_data['status']}. Response: {response_data}"
    assert response_data["errors"]["login"][0] == "The email and password combination cannot be authenticated", \
        f"Unexpected error message: {response_data['errors']['login'][0]}"


def test_invalid_password():
    # Test to verify login fails with incorrect password, even if the email is valid

    invalid_password_payload = {
        "email": "fo1_test_user@whatever.com",
        "password": "eבדיקהst"
    }

    response = requests.post(login_url, json=invalid_password_payload)
    response_data = response.json()

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}. Response: {response_data}"
    assert response_data["status"] == "error", f"Expected error status, got {response_data['status']}. Response: {response_data}"
    assert response_data["errors"]["login"][0] == "The login credentials provided are incorrect. If you forgot your password, use the link below to recover it.", \
        f"Unexpected error message: {response_data['errors']['login'][0]}"


def test_invalid_email_and_password_credentials():
    # Test to verify login fails when both email and password are invalid

    invalid_email_and_password_payload = {
        "email": "Test@userwhatever.com",
        "password": "test"
    }

    response = requests.post(login_url, json=invalid_email_and_password_payload)
    response_data = response.json()

    assert response.status_code == 400, "Invalid credentials, login should fail"
    assert response_data["status"] == "error", f"Expected error status, got {response_data['status']}. Response: {response_data}"
    assert response_data["errors"]["login"][0] == "The login credentials provided are incorrect. If you forgot your password, use the link below to recover it.", \
        f"Unexpected error message: {response_data['errors']['login'][0]}"


def test_max_failed_login_attempts():
    # Test to verify that after a certain number of failed login attempts, a lockout message is returned

    invalid_payload = {
        "email": "Test@userwhatever.com",
        "password": "test"
    }

    failed_attempts = 0
    while True:
        response = requests.post(login_url, json=invalid_payload)
        response_data = response.json()

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response_data}"

        if "Too many failed login attempts" in response_data['errors']['login'][0]:
            print(f"Lockout triggered after {failed_attempts} failed attempts")
            break

        if failed_attempts >= 5:
            assert response_data['errors']['login'][0] == "Too many failed login attempts. Please try again in 15 minutes.",\
                "More than 5 failed attempts without lock"
            break

        failed_attempts += 1
        time.sleep(1)

# List of Deals Tests

def test_verify_list_deals(get_auth_token):
    # Verify retrieval of deals using a valid authentication token

    headers = {
        "Authorization": f"Bearer {get_auth_token}"
    }

    response = requests.post(deals_list_url, headers=headers)
    response_data = response.json()

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response_data}"
    assert len(response_data['data']) == 1, (f"Expected exactly 1 deal, got {len(response_data['data'])}. "
                                             f"Response: {response_data}")
    assert response_data['data'][0]['title'] == "Shared deal for home assignment", \
        f"Unexpected deal title: {response_data['data'][0]['title']}"


def test_verify_list_deals_without_token():
    # Verify that accessing deals list without a token fails

    response = requests.post(deals_list_url)

    try:
         response_data = response.json()
    except Exception as e:
        print(str(e))

    assert response.status_code == 401, f"Expected status code 401 or 409, but got {response.status_code}"


def test_answered_sort(get_auth_token):
    # Test to validate the "answered" filter functionality

    answered_url = "https://fo1.api.altius.finance/api/v0.0.3/deals/5644/forms/5363?filter=answered"

    headers = {
        'Authorization': f"Bearer {get_auth_token}"
    }

    response = requests.get(answered_url, headers=headers)
    response_data = response.json()

    assert response.status_code == 200, f"Expected get 200, got instead {response.status_code}"
    assert 'data' in response_data, f"Expected tada in response. Response: {response_data}"
    assert 'message' in response_data and 'Successful' in response_data.get('message'), (f"Expected 'Successful',"
                                                     f" got instead {response_data['message']}. Response: {response_data}")

def test_post_comment(get_auth_token):
    # Test to validate the posting of a new comment

    post_url = "https://fo1.api.altius.finance/api/v0.0.3/deals/5644/comments"

    headers = {
        'Authorization': f"Bearer {get_auth_token}"
    }

    payload = {
        'audience': "tenants_team",
        'form_id': 5363,
        'question_id': 75339,
        'section_id': 16051,
        'text': "Here is a comment to post"
    }

    response = requests.post(post_url, headers=headers, json=payload)
    response_data = response.json()

    assert response.status_code == 201,  f"Expected status code 201, got {response.status_code}. Response: {response_data}"
    assert 'Successful' in response_data['message'], (f"Expected 'Successful', got instead {response_data['message']}. "
                                                      f"Response: {response_data}")

    data = response_data.get('data')
    assert data.get('text') == "Here is a comment to post", (f"Expected 'text' to be 'Here is a comment to post', "
                                                             f"but got {data.get('text')}. Response: {response_data}")


def test_update_comment(post_comment_id, get_auth_token):
    # Test to validate the functionality of updating a comment

    comment_id = post_comment_id
    update_url = f"https://fo1.api.altius.finance/api/v0.0.3/deals/5644/comments/{comment_id}"

    headers = {
        'Authorization': f"Bearer {get_auth_token}"
    }

    payload = {
        "form_id": 5363,
        "text": "Here is a comment but updated",
        "audience": "tenants_team"
    }

    response = requests.patch(update_url, headers=headers, json=payload)
    response_data = response.json()

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response_data}"
    assert 'Successful' in response_data.get('message'), (f"Expected 'Successful', "
                                                          f"got instead {response_data['message']}. Response: {response_data}")

    data = response_data.get('data')
    assert data.get('text') == "Here is a comment but updated", \
        f"Expected 'text' to be 'Here is a comment but updated', but got {data.get('text')}. Response: {response_data}"

def test_delete_comment(post_comment_id, get_auth_token):
    # Test to validate the deletion of a specific comment

    comment_id = post_comment_id
    delete_url = f"https://fo1.api.altius.finance/api/v0.0.3/deals/5644/comments/{comment_id}"

    headers = {
        'Authorization': f"Bearer {get_auth_token}"
    }

    response = requests.delete(delete_url, headers=headers)
    response_data = response.json()

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response_data}"

    assert 'data' in response_data and len(response_data.get('data')) == 0, \
        f"Expected no tada in response, got {response_data.get('data')}. Response: {response_data}"

    assert 'Successful' in response_data.get('message'), (f"Expected 'Successful', got instead {response_data['message']}."
                                                          f" Response: {response_data}")