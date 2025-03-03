from objective.objective import SPORT_IDS
from objective.validator import (
    validate_objective,
    validate_phase,
    validate_set_value,
    ValidationError,
)
from datetime import datetime
from typing import List, Optional


class PhaseBuilder:
    @staticmethod
    def create_phase(
        name: str,
        goal_type: str,
        phase_change_type: Optional[str] = "AUTOMATIC",
        intensity_type: Optional[str] = "HEART_RATE_ZONES",
        distance: Optional[int] = None,
        duration: Optional[str] = None,
        lower_zone: Optional[int] = None,
        upper_zone: Optional[int] = None,
    ):
        """
        Params:
            goal_type - ["DISTANCE", "DURATION"]
            phase_change_type - ["AUTOMATIC", "MANUAL"]
            intensity_type - ["HEART_RATE_ZONES", "NONE"]
            distance - number in meters
            duration - "HH:MM:SS"
            lower_zone - 1 to 5
            upper_zone - 1 to 5
        """
        phase = {
            "phaseType": "PHASE",
            "name": name,
            "goalType": goal_type,
            "phaseChangeType": phase_change_type,
            "intensityType": intensity_type,
            "distance": distance,
            "duration": duration,
            "lowerZone": lower_zone,
            "upperZone": upper_zone,
        }
        validate_phase(phase)
        return phase

    @staticmethod
    def create_repeat_phase(repeat_count: int, phases: List[dict]):
        if not phases:
            raise ValidationError("Repeat phases must contain at least one phase.")
        if phases[-1]["phaseType"] != "PHASE":
            raise ValidationError(
                "The last phase in a repeat phase must be of type 'PHASE'."
            )
        return {"phaseType": "REPEAT", "repeatCount": repeat_count, "phases": phases}


class ExerciseTargetBuilder:
    def __init__(self):
        self._exercise_target = {
            "sportId": None,
            "distance": None,
            "duration": None,
            "phases": [],
            "calories": None,  # Unchanged value
            "id": None,  # Unchanged value
        }

    def with_sport_id(self, sport_name: str):
        """
        Params:
            sport_name - ["run", "run treadmill", "cycling", "strength",
                          "swim", "open water swim", "swim in pool"]
        """
        validate_set_value(sport_name, SPORT_IDS)
        self._exercise_target["sportId"] = SPORT_IDS[sport_name]
        return self

    def with_distance(self, distance: int):
        """
        Params:
            distance - number in meters
        """
        self._exercise_target["distance"] = distance
        return self

    def with_duration(
        self,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ):
        if minutes >= 60 or seconds >= 60:
            raise ValidationError("Minutes and seconds must be less than 60.")
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.exercise_target["duration"] = duration_str
        return self

    def add_phase(self, phase: dict):
        self._exercise_target["phases"].append(phase)
        return self

    def _build(self):
        return self._exercise_target


class ObjectiveBuilder:
    def __init__(self):
        self._schema = {
            "type": None,
            "name": None,
            "description": None,
            "datetime": None,
            "exerciseTargets": [],
        }
        self.date_str = datetime.now().strftime("%Y-%m-%d")  # Default to today's date
        self.time_str = "17:00"  # Default to 5 PM

    def with_type(self, type: str):
        validate_set_value(type, ["PHASED", "VOLUME", "STEADY_RACE_PACE"])
        self._schema["type"] = type
        return self

    def with_name(self, name: str):
        self._schema["name"] = name
        return self

    def with_description(self, description: str):
        self._schema["description"] = description
        return self

    def with_date(self, date_str: str, date_format: str = "%Y-%m-%d"):
        datetime.strptime(date_str, date_format)  # Validate the date format
        self.date_str = date_str
        return self

    def with_time(self, time_str: str = "17:00", time_format: str = "%H:%M"):
        datetime.strptime(time_str, time_format)  # Validate the time format
        self.time_str = time_str
        return self

    def add_target(self, target: ExerciseTargetBuilder):
        self._schema["exerciseTargets"].append(target._build())
        return self

    def build(self) -> dict:
        def build_datetime(self):
            datetime_obj = datetime.strptime(
                f"{self.date_str} {self.time_str}", "%Y-%m-%d %H:%M"
            )
            self._schema["datetime"] = datetime_obj.isoformat()

        build_datetime(self)
        validate_objective(self._schema)
        return self._schema
