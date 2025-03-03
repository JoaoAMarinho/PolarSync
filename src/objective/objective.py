SPORT_IDS = {
    "run": 1,
    "run treadmill": 17,
    "cycling": 2,
    "strength": 15,
    "swim": 23,
    "open water swim": 105,
    "swim in pool": 103,
}

SCHEMA = """
{
  "type": "object",
  "properties": {
    "type": {
      "type": "string",
      "enum": ["PHASED", "VOLUME", "STEADY_RACE_PACE"]
    },
    "name": { "type": "string" },
    "description": { "type": "string" },
    "datetime": {
      "type": "string",
      "format": "date-time"
    },
    "exerciseTargets": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "distance": { "type": ["number", "null"] },
          "calories": { "type": ["number", "null"] },
          "phases": {
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "phaseType": { "type": "string", "enum": ["PHASE"] },
                    "name": { "type": "string" },
                    "phaseChangeType": { "type": "string", "enum": ["AUTOMATIC", "MANUAL"] },
                    "goalType": { "type": "string", "enum": ["DISTANCE", "DURATION"] },
                    "distance": { "type": ["number", "null"] },
                    "duration": { "type": ["string", "null"] },
                    "intensityType": { "type": "string", "enum": ["HEART_RATE_ZONES", "NONE"] },
                    "lowerZone": { "type": ["number", "null"] },
                    "upperZone": { "type": ["number", "null"] }
                  },
                  "required": ["phaseType", "name", "phaseChangeType", "goalType", "intensityType"]
                },
                {
                  "type": "object",
                  "properties": {
                    "phaseType": { "type": "string", "enum": ["REPEAT"] },
                    "repeatCount": { "type": "integer", "minimum": 1 },
                    "phases": {
                      "type": "array",
                      "items": { "$ref": "#" }
                    }
                  },
                  "required": ["phaseType", "repeatCount", "phases"]
                }
              ]
            }
          },
          "sportId": {
            "type": "integer",
            "enum": [1 (Run), 17 (Run Treadmill), 2 (Cycle), 15 (Strength), 23 (Swim), 105 (Open Water Swim), 103 (Swim pool)]
          },
          "duration": { "type": ["string", "null"] },
          "id": { "type": ["number", "null"] }
        },
        "required": ["phases", "sportId"]
      }
    }
  },
  "required": ["type", "name", "description", "datetime", "exerciseTargets"]
}
"""
