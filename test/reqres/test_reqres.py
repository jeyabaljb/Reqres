import pytest
import logging
from src.utils.api_client import APIS
from src.utils.data_loader import get_payload_by_name
from src.utils.assertions import *
from src.utils.schema_validator import *

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def apis():
    logger.info("Initializing APIS fixture")
    return APIS()


pytest.mark.smoke()
def test_post_reqres(apis):
    logger.info("Running test: test_post_reqres")
    payload=get_payload_by_name("test_reqres_post", "payload_reqres.json", "reqres_payload")
    response=apis.post(payload)

    schema_post_reqres(response)
    assert_valid_response(response)

    logger.info("test_post_ach passed successfully")


pytest.mark.smoke()
def test_get_reqres(apis):
   logger.info("Running test: test_get_reqres")
   response=apis.get("?page=1")

   schema_get_reqres(response)
   assert_valid_response(response)

   logger.info("test_post_ach passed successfully")


pytest.mark.smoke()
def test_get2_reqres(apis):
    logger.info("Running test: test_get2_reqres")
    response=apis.get("2")

    schema_get2_reqres(response)
    assert_valid_response(response)

    logger.info("test_get2_reqres passed successfully")


pytest.mark.regression()
def test_get_user_not_found(apis):
    logger.info("Running test: test_get_user_not_found")
    response =apis.get("/9999")  # Non-existent user

    assert_negative_status(response, allowed_statuses=[404])

    logger.info("test_post_ach passed successfully")


pytest.mark.regression()
def test_get_users_invalid_query_format(apis):
    logger.info("Running test: test_get_users_invalid_query_format")
    response = apis.get("12345?")

    assert_negative_status(response, allowed_statuses=[400, 404])

    logger.info("test_get_users_invalid_query_format passed successfully")