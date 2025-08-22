import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Automatically find "data" and "schema" folder no matter where it is
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]  # go up 2 levels from utils/
DATA_DIR = (PROJECT_ROOT / "src" / "data") if (PROJECT_ROOT / "src" / "data").exists() else (PROJECT_ROOT / "data")
SCHEMA_DIR = (PROJECT_ROOT / "src" / "schema") if (PROJECT_ROOT / "src" / "schema").exists() else (PROJECT_ROOT / "schema")

def get_payload_by_name(name: str, file_name: str, folder: str) -> dict:
    # Use the DATA_DIR from your config
    folder_path = DATA_DIR / folder

    if not folder_path.is_dir():
        logger.error(f"Folder '{folder}' not found under '{DATA_DIR}/'")
        raise FileNotFoundError(f"Folder '{folder}' not found under '{DATA_DIR}/'")

    file_path = folder_path / file_name

    if not file_path.exists():
        logger.error(f"Payload file not found at path: {file_path}")
        raise FileNotFoundError(f"Payload file not found at path: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            payloads = json.load(f)
        logger.info(f"Payload file '{file_name}' loaded successfully")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in file: {file_path} | Error: {e}")
        raise ValueError(f"Invalid JSON format in file: {file_path}")

    if name not in payloads:
        logger.error(f"Payload '{name}' not found in file '{file_name}' under folder '{folder}'")
        raise ValueError(f"Payload '{name}' not found in file '{file_name}' under folder '{folder}'")

    logger.info(f"Payload '{name}' retrieved successfully from file '{file_name}'")
    return payloads[name]


def get_schema_by_name(schema_name: str, file_name: str, folder: str) -> dict:

    folder_path = SCHEMA_DIR / folder

    if not folder_path.is_dir():
        logger.error(f"Folder '{folder}' not found under '{DATA_DIR}/'")
        raise FileNotFoundError(f"Folder '{folder}' not found under '{DATA_DIR}/'")

    schema_path = folder_path / file_name

    if not schema_path.exists():
        logger.error(f"Schema file not found at path: {schema_path}")
        raise FileNotFoundError(f"Schema file not found at path: {schema_path}")

    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schemas = json.load(f)
        logger.info(f"Schema file '{file_name}' loaded successfully")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in file: {schema_path} | Error: {e}")
        raise ValueError(f"Invalid JSON format in file: {schema_path}")

    if schema_name not in schemas:
        logger.error(f"Schema '{schema_name}' not found in file '{file_name}' under folder '{folder}'")
        raise ValueError(f"Schema '{schema_name}' not found in file '{file_name}' under folder '{folder}'")

    logger.info(f"Schema '{schema_name}' retrieved successfully from file '{file_name}'")
    return schemas[schema_name]