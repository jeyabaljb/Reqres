import re
from datetime import datetime
import logging
from src.utils.data_loader import get_schema_by_name
from src.utils.schema_validator import validate_json_schema

logger = logging.getLogger(__name__)

def assert_valid_response(response):
    method = response.request.method.upper()
    print(f"HTTP method: {method}")
    expected_status_map = {
        "GET": 200,
        "POST": [200, 201],
        "PUT": 200,
        "PATCH": 200,
        "DELETE": 204,
    }
    if method not in expected_status_map:
        raise ValueError(f"Unsupported HTTP method: {method}")
    expected_status = expected_status_map[method]
    msg = f"Status was {response.status_code}, expected {expected_status}"
    assert response.status_code == expected_status, msg
    try:
        data = response.json()
    except ValueError:
        assert False, "Response did not contain valid JSON"
    assert data, "Response JSON is empty"
    if method == "GET":

        # Validating schema
        schema = get_schema_by_name("get_ach", "schema_reqres.json", "reqres_schema")
        is_valid, error = validate_json_schema(data, schema)
        if is_valid:
            logger.info("Schema Validation passed successfully")
        else:
            logger.error(f"Validation failed:{error}")

        required_fields = ["paymentId", "paymentStatus", "statusUpdatedAt", "requestedExecutionDate",
                           "endToEndId", "transferType", "paymentType"]
        for field in required_fields:
            assert field in data, f"Missing'{field}' in response"
            assert isinstance(data[field], str), f"'{field}' must be a string"
        assert datetime.strptime(data["requestedExecutionDate"], "%Y-%m-%d") and len(
            data["requestedExecutionDate"]) == 10
        assert "endToEndId" in data, "Missing 'endToEndId' in response"
        assert 1 <= len(data["endToEndId"]) <= 16, f"'endToEndId' is not between 1 and 16"
        assert data["endToEndId"].isalnum(), f"'endToEndId' is {data['endToEndId']}"
        assert "transferType" in data, "Missing 'transferType' in response"
        assert "paymentType" in data, "Missing 'paymentType' in response"
    elif method == "POST":

        # Validating schema
        schema = get_schema_by_name("post_ach", "schema_reqres.json", "reqres_schema")
        is_valid, error = validate_json_schema(data, schema)
        if is_valid:
            logger.info("Schema Validation passed successfully")
        else:
            logger.error(f"Validation failed:{error}")

        # Assert keys are present
        assert "endToEndId" in data, "Missing 'endToEndId' in response"
        end_to_end_id = data["endToEndId"]
        assert isinstance(end_to_end_id, str), "'endToEndId' should be a string"
        assert 1 <= len(
            end_to_end_id) <= 35, f"'endToEndId' length should be between 1 and 35, got {len(end_to_end_id)}"
        assert "paymentId" in data, "Missing 'paymentId' in response"
        payment_id = data["paymentId"]
        assert isinstance(payment_id, str), "'paymentId' should be a string"
        assert re.fullmatch(
            r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
            payment_id,
            re.IGNORECASE
        ), f"'paymentId' is not a valid UUIDv4: {payment_id}"
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

def assert_expected_response(response, expected_json):
    assert response.json() == expected_json, "Response JSON did not match expected"

def assert_valid_headers(response, expected_headers):
    response_headers = {k.lower(): v for k, v in response.headers.items()}
    for key, expected_value in expected_headers.items():
        actual_value = response_headers.get(key.lower())
        assert actual_value == expected_value, (
            f"Header mismatch for '{key}': expected '{expected_value}', got '{actual_value}'")