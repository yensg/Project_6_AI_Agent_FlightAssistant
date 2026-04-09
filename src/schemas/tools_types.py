from pydantic import BaseModel, field_validator
from typing import Optional, Literal

class GetFlightDetailsArgs(BaseModel):
    flight_number: Optional[str] = None
    callsign: Optional[str] = None
    icao24: Optional[str] = None
    date: Optional[str] = None
    airport: Optional[str] = None

    @field_validator("*", mode="before")
    @classmethod
    def normalize_strings(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return str(v).strip() or None


FlightDirection = Literal["arrival", "departure"]

class SearchFlightsArgs(BaseModel):
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    airport: Optional[str] = None
    direction: Optional[FlightDirection] = None
    origin_city: Optional[str] = None
    destination_city: Optional[str] = None
    date: Optional[str] = None
    time_from: Optional[str] = None
    time_to: Optional[str] = None
    max_results: Optional[int] = None

    @field_validator("*", mode="before")
    @classmethod
    def normalize_fields(cls, v):
        if v in ("", None):
            return None
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return v

class CountFlightsArgs(BaseModel):
    airport: Optional[str] = None
    direction: Optional[FlightDirection] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    date: Optional[str] = None

    @field_validator("*", mode="before")
    @classmethod
    def normalize_fields(cls, v):
        if v in ("", None):
            return None
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return v

class ListFlightsArgs(BaseModel):
    airport: Optional[str] = None
    direction: Optional[FlightDirection] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    date: Optional[str] = None
    time_from: Optional[str] = None
    time_to: Optional[str] = None
    max_results: Optional[int] = None

    @field_validator("*", mode="before")
    @classmethod
    def normalize_fields(cls, v):
        if v in ("", None):
            return None
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return v

TOOL_ARG_MODELS = {
    "get_flight_details": GetFlightDetailsArgs,
    "search_flights": SearchFlightsArgs,
    "count_flights": CountFlightsArgs,
    "list_flights": ListFlightsArgs,
}