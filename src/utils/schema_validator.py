import logging
from jsonschema import validate, ValidationError
from src.utils.data_loader import get_schema_by_name

logger = logging.getLogger(__name__)


def validate_json_schema(response, schema):
    try:
        logger.info("Schema validation running")
        method = response.request.method.upper()
        print(f"HTTP method: {method}")
        expected_status_map = {
            "GET": 200,
            "POST": 201,
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
            instance = response.json()
        except ValueError:
            assert False, "Response did not contain valid JSON"
        assert instance, "Response JSON is empty"
        validate(instance=instance, schema=schema)
        return True, None
    except ValidationError as e:
        logger.error("")
        return False, e.message


def schema_get_reqres(response):
    schema = get_schema_by_name("GET_REQRES", "schema_reqres.json", "reqres_schema")
    is_valid, error = validate_json_schema(response, schema)
    if is_valid:
        logger.info("Schema Validation passed successfully")
    else:
        logger.error(f"Validation failed:{error}")


def schema_get2_reqres(response):
    schema = get_schema_by_name("GET2_REQRES", "schema_reqres.json", "reqres_schema")
    is_valid, error = validate_json_schema(response, schema)
    if is_valid:
        logger.info("Schema Validation passed successfully")
    else:
        assert False, f"validation failed: {error}"


def schema_post_reqres(response):
    schema = get_schema_by_name("POST_REQRES", "schema_reqres.json", "reqres_schema")
    is_valid, error = validate_json_schema(response, schema)
    if is_valid:
        logger.info("Schema Validation passed successfully")
    else:
        assert False, f"validation failed: {error}"



