class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


def _has_required_fields(dict: dict, fields: list):
    for field in fields:
        if dict[field] is None or dict[field] == "":
            raise ValidationError(f"Field '{field}' is required.")


def _has_correctly_defined_type(objective):
    if objective["type"] != "PHASED":
        if len(objective["exerciseTargets"][""]) != 1:
            raise ValidationError(
                "Non-PHASED types must have exactly one exerciseTarget."
            )
        for target in objective["exerciseTargets"]:
            if target["phases"]:
                raise ValidationError(
                    "Non-PHASED types must have empty phases in exerciseTargets."
                )

    target = objective["exerciseTargets"][0]
    if objective["type"] == "VOLUME":
        if target["distance"] is None and target["duration"] is None:
            raise ValidationError(
                "For type 'VOLUME', either distance or duration must be provided."
            )
        elif target["distance"] and target["duration"]:
            raise ValidationError(
                "For type 'VOLUME', only one of distance and duration must be provided."
            )
    elif objective["type"] == "STEADY_RACE_PACE":
        if target["distance"] is None or target["duration"] is None:
            raise ValidationError(
                "For type 'STEADY_RACE_PACE', both distance and duration must be provided."
            )


def validate_objective(objective):
    required_fields = ["type", "name", "description", "datetime", "exerciseTargets"]
    _has_required_fields(objective, required_fields)
    _has_correctly_defined_type(objective)


def validate_set_value(value, list: list):
    if value not in list:
        raise ValidationError(f"Invalid value: {value}.\nMust be one of:\n\t{list}")


def _validate_zones(requires_zones, lower_zone, upper_zone):
    if requires_zones:
        if lower_zone is None or upper_zone is None:
            raise ValidationError(
                "Intensity type 'HEART_RATE_ZONES' requires a value for lower and upper zones."
            )
        if not (0 < lower_zone < 6) or not (0 < upper_zone < 6):
            raise ValidationError(
                "lower_zone and upper_zone must be greater than 0 and less than 6."
            )

        if lower_zone > upper_zone:
            raise ValidationError(
                "lower_zone must be less than or equal to upper_zone."
            )
    else:
        if lower_zone is not None or upper_zone is not None:
            raise ValidationError(
                "Intensity type 'NONE' requires lower and upper zones set to None."
            )


def _validate_phase_type_values(phase: dict):
    goal_type = phase["goalType"]
    if goal_type == "DISTANCE" and phase["distance"] is None:
        raise ValidationError("Phase with 'DISTANCE' goal must set distance value.")
    if goal_type == "DURATION" and phase["duration"] is None:
        raise ValidationError("Phase with 'DURATION' goal must set distance value.")


def validate_phase(phase: dict):
    required_fields = [
        "phaseType",
        "name",
        "goalType",
        "phaseChangeType",
        "intensityType",
        "lowerZone",
        "upperZone",
    ]
    _has_required_fields(phase, required_fields)
    validate_set_value(phase["goalType"], ["DISTANCE", "DURATION"])
    validate_set_value(phase["phaseChangeType"], ["AUTOMATIC", "MANUAL"])
    validate_set_value(phase["intensityType"], ["HEART_RATE_ZONES", "NONE"])
    _validate_zones(
        phase["intensityType"] == "HEART_RATE_ZONES",
        phase["lowerZone"],
        phase["upperZone"],
    )
    _validate_phase_type_values(phase)
