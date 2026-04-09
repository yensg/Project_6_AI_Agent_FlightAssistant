# src/schemas/context/json_schema.py

CONTEXT_UPDATE_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "domain": {
            "type": "string",
            "enum": ["flight"]
        },
        "intent": {
            "type": "string",
            "enum": [
                "get_flight_details",
                "search_flights",
                "count_flights",
                "list_flights",
                "clarify"
            ]
        },
        "entities": {
            "type": "object",
            "properties": {
                "flight_number": {"type": ["string", "null"]},
                "callsign": {"type": ["string", "null"]},
                "icao24": {"type": ["string", "null"]},
                "airline": {"type": ["string", "null"]},
                "airport": {"type": ["string", "null"]},
                "departure_airport": {"type": ["string", "null"]},
                "arrival_airport": {"type": ["string", "null"]},
                "direction": {
                    "type": ["string", "null"],
                    "enum": ["arrival", "departure", None]
                },
                "origin_city": {"type": ["string", "null"]},
                "destination_city": {"type": ["string", "null"]},
                "date": {"type": ["string", "null"]},
                "local_day": {
                    "type": ["string", "null"],
                    "enum": ["today", "tomorrow", "yesterday", None]
                },
                "time_from": {"type": ["string", "null"]},
                "time_to": {"type": ["string", "null"]}
            },
            "additionalProperties": False
        },
        "aggregation": {
            "type": "string",
            "enum": [
                "count",
                "group_by_airline",
                "group_by_origin",
                "group_by_destination",
                "none"
            ]
        },
        "preferences": {
            "type": "object",
            "properties": {
                "timezone": {"type": ["string", "null"]},
                "response_mode": {
                    "type": ["string", "null"],
                    "enum": ["summary", "detailed", None]
                },
                "max_results": {"type": ["integer", "null"]}
            },
            "additionalProperties": False
        },
        "inferred_defaults": {
            "type": "object",
            "properties": {
                "airport": {"type": ["string", "null"]},
                "direction": {
                    "type": ["string", "null"],
                    "enum": ["arrival", "departure", None]
                }
            }
        },
        "missing_slots": {
            "type": "array",
            "items": {"type": "string"}
        },
        "requires_tool": {"type": ["boolean", "null"]},
        "confidence": {"type": ["number", "null"]}
    },
    "required": ["intent", "entities"],
    "additionalProperties": False
}