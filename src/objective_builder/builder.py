# objective_builder/builder.py


class WorkoutObjectiveBuilder:
    def __init__(self):
        self.workout_data = {
            "type": "PHASED",
            "name": "Workout name",
            "datetime": "2025-02-26T10:00:00",
            "description": "This is a sample workout",
            "exerciseTargets": [],
        }

    def add_exercise_target(self, sport_id, phases):
        self.workout_data["exerciseTargets"].append(
            {
                "sportId": sport_id,
                "distance": None,
                "calories": None,
                "duration": None,
                "id": None,
                "phases": phases,
            }
        )
        return self

    def build(self):
        return self.workout_data
