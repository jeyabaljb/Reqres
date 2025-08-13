import os
import requests
import logging

logger = logging.getLogger(__name__)  # Get module-specific logger

class APIS:
    def __init__(self, token=None):
        # Read the base URL from the .env.qa.QA file
        self.base_url = os.getenv("BASE_URL")
        if not self.base_url:
            logger.error("BASE_URL is not set in environment variables.")
            raise ValueError("BASE_URL must be set in the .env.qa file")

        # Set up base headers from environment variables
        self.base_headers = {
            "Content-Type": os.getenv("CONTENT_TYPE"),
            "Accept": os.getenv("ACCEPT"),
            "x-api-key": "reqres-free-v1"
        }

        # If an auth token is provided, add it to headers as Bearer token
        auth_token = token or os.getenv("AUTH_TOKEN")
        if auth_token:
            self.base_headers["Authorization"] = f"Bearer {auth_token}"
            logger.info("Authorization token added to headers.")
        else:
            logger.warning("No Authorization token found. Requests may fail if auth is required.")

        logger.info("API client initialized with base URL: %s", self.base_url)

    def get(self, endpoint): #Get request function
        # Construct full URL using base URL + endpoint
        url = f"{self.base_url}/{endpoint}"
        logger.info("Sending GET request to URL: %s", url)

        # Send GET request with headers
        try:
            response = requests.get(url, headers=self.base_headers)
            logger.info("GET response received with status code: %d", response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request failed for {url}: {e}")
            raise RuntimeError(f"GET request failed for {url}: {e}")

    def post(self, payload): #Post request function
        # Construct full URL using base URL + endpoint
        url = f"{self.base_url}"
        logger.info("Sending POST request to URL: %s", url)

        # Create a fresh copy of base headers to modify for this request
        headers = self.base_headers.copy()

        logger.info("Sending POST request to URL: %s", url)

        # Send POST request with headers and JSON body
        try:
            response = requests.post(url, headers=headers, json=payload)
            logger.info("POST response received with status code: %d", response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request failed for {url}: {e}")
            raise RuntimeError(f"POST request failed for {url}: {e}")