import pytest
from src.utils.api_client import APIS
from src.utils.data_loader import get_payload_by_name, get_schema_by_name
from src.utils.assertions import *
from src.utils.schema_validator import schema_post_reqres, schema_get_reqres

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

    logger.info("test_post_ach passed successfully")


def test_get_reqres(apis):
   logger.info("Running test: test_get_reqres")
   response=apis.get("?page=1")

   schema_get_reqres(response)

   logger.info("test_post_ach passed successfully")




