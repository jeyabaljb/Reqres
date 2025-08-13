import pytest
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from src.utils.logger import setup_logger

logger = setup_logger()

load_dotenv()

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="QA",
        help="Environment to run tests against: qa or uat"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):

    # Configure pytest before running tests
    # Load environment variables from the correct .env.qa.* file
    env = config.getoption("--env")  # Read the environment from CLI
    env_file = f".env.{env}"
    if os.path.exists(env_file):
        load_dotenv(env_file)
        logger.info(f"Loaded environment variables from {env_file}")
    else:
        logger.warning(f"{env_file} not found. Falling back to .env.qa.QA file.")
        load_dotenv("../.env.qa")

    # Always create reports folder inside project root
    project_root = Path(__file__).resolve().parent.parent  # go up to root
    report_dir = project_root / "reports"
    report_dir.mkdir(exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    config.option.htmlpath = f"{report_dir}/reports_{now}.html"

    # logger.info(f"pytest_configure executed for environment: {env}")
    logger.info(f"HTML report will be generated at: {config.option.htmlpath}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.failed:
            logger.error(f"Test FAILED: {item.name}")
        elif report.passed:
            logger.info(f"Test PASSED: {item.name}")


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    logger.info("== Test Session START ==")
    yield
    logger.info("== Test Session END ==")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Custom summary at the end of pytest run
    """
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))

    logger.info("==== Custom Test Summary ====")
    logger.info(f"Total tests collected: {total}")
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")

    terminalreporter.write("\n\n==== Custom Test Summary ====\n")
    terminalreporter.write(f"Total tests collected: {total}\n")
    terminalreporter.write(f"Passed: {passed}\n")
    terminalreporter.write(f"Failed: {failed}\n")
    terminalreporter.write("=============================\n")
