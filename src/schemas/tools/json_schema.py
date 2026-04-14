GET_FLIGHT_DETAILS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_flight_details",
        "description": "Get details for a specific flight using identifiers like flight number, callsign, or icao24.",
        "parameters": {
            "type": "object",
            "properties": {
                "flight_number": {"type": "string"},
                "callsign": {"type": "string"},
                "icao24": {"type": "string"},
                "date": {"type": "string"},
                "airport": {"type": "string"}
            },
            "required": []
        }
    }
}

SEARCH_FLIGHTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "Search flights by departure airport, arrival airport, direction, date, or city pair.",
        "parameters": {
            "type": "object",
            "properties": {
                "departure_airport": {"type": "string"},
                "arrival_airport": {"type": "string"},
                "airport": {"type": "string"},
                "direction": {
                    "type": "string",
                    "enum": ["arrival", "departure"]
                },
                "origin_city": {"type": "string"},
                "destination_city": {"type": "string"},
                "date": {"type": "string"},
                "time_from": {"type": "string"},
                "time_to": {"type": "string"},
                "max_results": {"type": "integer"}
            },
            "required": []
        }
    }
}

COUNT_FLIGHTS_TOOL = {
    "type": "function",
    "function": {
        "name": "count_flights",
        "description": "Count flights matching the given filters.",
        "parameters": {
            "type": "object",
            "properties": {
                "airport": {"type": "string"},
                "direction": {
                    "type": "string",
                    "enum": ["arrival", "departure"]
                },
                "departure_airport": {"type": "string"},
                "arrival_airport": {"type": "string"},
                "date": {"type": "string"}
            },
            "required": []
        }
    }
}

LIST_FLIGHTS_TOOL = {
    "type": "function",
    "function": {
        "name": "list_flights",
        "description": "List flights matching the given filters.",
        "parameters": {
            "type": "object",
            "properties": {
                "airport": {"type": "string"},
                "direction": {
                    "type": "string",
                    "enum": ["arrival", "departure"]
                },
                "departure_airport": {"type": "string"},
                "arrival_airport": {"type": "string"},
                "date": {"type": "string"},
                "time_from": {"type": "string"},
                "time_to": {"type": "string"},
                "max_results": {"type": "integer"}
            },
            "required": []
        }
    }
}

FLIGHT_TOOLS = [
    GET_FLIGHT_DETAILS_TOOL,
    SEARCH_FLIGHTS_TOOL,
    COUNT_FLIGHTS_TOOL,
    LIST_FLIGHTS_TOOL,
]