import os
from dotenv import load_dotenv
from utils.logger import logger


def load_config():
    """
    Load user-specific configuration from the .env file.
    """
    # Load the .env file
    load_dotenv()

    # Read configuration values
    config = {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
    }

    # Validate that required values are present
    if not config["username"] or not config["password"]:
        raise ValueError("Missing required configuration in .env file.")

    logger.info("Parsed configuration.")
    return config
