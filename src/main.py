# main.py

from utils.logger import logger  # Global logger instance
from web.webdriver_manager import initialize_driver, close_driver
from web.navigation import login, navigate_to_workout_page, accept_cookies

# from api.workout_api import create_workout
from requests import Session
from objective_builder.builder import WorkoutObjectiveBuilder
from config.settings import (
    LOGIN_URL,
    WORKOUT_DATE_URL,
    TRAINING_TARGET_URL
)
from config.config_loader import load_config

def main():
    config = load_config()

    try:
    driver = initialize_driver()
        login(driver, config)

        # Assess Day
        navigate_to_workout_page(driver)

        session = Session()
        accept_cookies(driver, session)

        # builder = WorkoutObjectiveBuilder()
        # workout_data = builder.add_exercise_target(
        #     sport_id=1,
        #     phases=[
        #         {
        #             "phaseType": "REPEAT",
        #             "repeatCount": 2,
        #             "phases": [
        #                 {
        #                     "distance": 21000,
        #                     "duration": None,
        #                     "goalType": "DISTANCE",
        #                     "intensityType": "HEART_RATE_ZONES",
        #                     "lowerZone": 1,
        #                     "name": "Phase name",
        #                     "phaseChangeType": "AUTOMATIC",
        #                     "phaseType": "PHASE",
        #                     "upperZone": 1,
        #                 }
        #             ],
        #         }
        #     ]
        # ).build()

        # response = create_workout(session, workout_data)

        # if response.status_code == 201:
        #     logger.info("Workout created successfully!")
        # else:
        #     logger.error("Failed to create workout.")
        #     logger.error(f"Status Code: {response.status_code}")
        #     logger.error(f"Response: {response.text}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        close_driver(driver)


if __name__ == "__main__":
    main()
