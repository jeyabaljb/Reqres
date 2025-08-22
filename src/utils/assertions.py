import logging

logger = logging.getLogger(__name__)

def assert_valid_response(response):
    method = response.request.method.upper()
    expected_status_map = {
        "GET": 200,
        "POST": 201,
        "PUT": 200,
        "PATCH": 200,
        "DELETE": 204,
    }

    if method not in expected_status_map:
        raise ValueError(f"Unsupported HTTP method: {method}")

    # Assert status code
    expected_status = expected_status_map[method]
    msg = f"Status was {response.status_code}, expected {expected_status}"
    assert response.status_code == expected_status, msg
    # Assert response time
    max_response_time = 2
    response_time = response.elapsed.total_seconds()
    assert response_time < max_response_time, f"Response time {response_time}s exceeded {max_response_time}s"

    # Validate response has valid JSON
    try:
        data = response.json()
    except ValueError:
        assert False, "Response did not contain valid JSON"


def assert_expected_response(response, expected_json):
    assert response.json() == expected_json, "Response JSON did not match expected"

def assert_valid_headers(response, expected_headers: dict):
    response_headers = {k.lower(): v for k, v in response.headers.items()}
    for key, expected_value in expected_headers.items():
        actual = response_headers.get(key.lower())
        assert actual == expected_value, (
            f"Header mismatch for '{key}': expected '{expected_value}', got '{actual}'"
        )

def assert_negative_status(response, allowed_statuses):
    status_code = response.status_code
    if status_code in allowed_statuses:
        print(f"[PASS] Status code: {status_code}")
    else:
        error_msg = (
            f"[FAIL] Expected one of {allowed_statuses}, but got {status_code}.\n"
            f"Response body: {response.text}"
        )
        assert False, error_msg