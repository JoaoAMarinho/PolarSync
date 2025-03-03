from requests import Session
from utils.logger import logger  # Global logger instance
from config.config_loader import load_config
from web.initializer import initialize_browser
from web.navigation import login, navigate_to_objective_target, accept_cookies
from web.api import create_training_objective
from objective.builder import ObjectiveBuilder, ExerciseTargetBuilder, PhaseBuilder


def main():
    config = load_config()
    browser = initialize_browser(background=False)

    try:
        login(browser, config)

        session = Session()
        target = (
            ExerciseTargetBuilder()
            .with_sport_id("run")
            .add_phase(
                PhaseBuilder.create_phase(
                    name="El nome",
                    goal_type="DISTANCE",
                    distance=10,
                    lower_zone=1,
                    upper_zone=1,
                )
            )
        )
        objective = (
            ObjectiveBuilder()
            .with_type("PHASED")
            .with_name("ok")
            .with_description("ok")
            .add_target(target)
            .with_date("2025-03-04")
            .build()
        )
        logger.info(f"Creating objective:\n\t{objective}\n")
        navigate_to_objective_target(browser, objective)
        accept_cookies(browser, session)
        create_training_objective(session, objective)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        session.close()
        browser.close()


if __name__ == "__main__":
    main()
