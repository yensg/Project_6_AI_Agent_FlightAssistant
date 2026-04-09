# src/schemas/context/canonical_schema.py

CANONICAL_CONTEXT_UPDATE_SCHEMA = {
    "domain": "flight",
    "intent": [
        "get_flight_details",
        "search_flights",
        "count_flights",
        "list_flights",
        "clarify"
    ],
    "entities": {
        "flight_number": "string | null",
        "callsign": "string | null",
        "icao24": "string | null",
        "airline": "string | null",
        "airport": "string | null",
        "departure_airport": "string | null",
        "arrival_airport": "string | null",
        "direction": "arrival | departure | null",
        "origin_city": "string | null",
        "destination_city": "string | null",
        "date": "string | null",
        "local_day": "today | tomorrow | yesterday | null",
        "time_from": "string | null",
        "time_to": "string | null"
    },
    "aggregation": [
        "count",
        "group_by_airline",
        "group_by_origin",
        "group_by_destination",
        "none"
    ],
    "preferences": {
        "timezone": "string | null",
        "response_mode": "summary | detailed | null",
        "max_results": "int | null"
    },
    "inferred_defaults": {
        "airport": "string | null",
        "direction": "arrival | departure | null"
    },
    "missing_slots": [
        "list of strings"
    ],
    "requires_tool": "bool | null",
    "confidence": "float | null"
}