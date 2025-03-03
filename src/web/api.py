import json
from datetime import datetime
from utils.logger import logger
from .constants import TRAINING_DATE_URL, TRAINING_TARGET_URL


def create_training_objective(session, objective: object):
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Referer": TRAINING_DATE_URL
        + datetime.fromisoformat(objective["datetime"]).strftime("%Y-%m-%d"),
        "X-XSRF-TOKEN": session.cookies.get("XSRF-TOKEN"),
    }
    response = session.post(
        TRAINING_TARGET_URL, data=json.dumps(objective), headers=headers
    )
    if response.status_code == 201:
        logger.info("Workout created successfully!")
    else:
        logger.error("Failed to create workout.")
        logger.error(f"Status Code: {response.status_code}")
        logger.error(f"Response: {response.text}")
    return response
