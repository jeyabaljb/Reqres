import logging

from src.utils.data_loader import get_schema_by_name

logger = logging.getLogger(__name__)

from jsonschema import validate, ValidationError

def validate_json_schema(instance, schema):
    try:
        logger.info("Schema validation running")
        validate(instance=instance, schema=schema)
        return True, None
    except ValidationError as e:
        logger.error("")
        return False, e.message


def schema_get_reqres(response):
    data=response.json()
    if response.status_code in [200, 201, 202]:
        schema = get_schema_by_name("GET_REQRES", "schema_reqres.json", "reqres_schema")
        is_valid, error = validate_json_schema(data, schema)
        if is_valid:
            logger.info("Schema Validation passed successfully")
        else:
            logger.error(f"Validation failed:{error}")

def schema_post_reqres(response):
    data = response.json()
    print(data)
    print(response.status_code)
    # Validating schema
    if response.status_code in [200, 201, 202]:
       schema = get_schema_by_name("POST_REQRES", "schema_reqres.json", "reqres_schema")
       is_valid, error = validate_json_schema(data, schema)
       if is_valid:
          logger.info("Schema Validation passed successfully")
       else:
           assert False, f"validation failed: {error}"



