from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, Literal
from datetime import datetime, timezone

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

# class SearchFlightsArgs(BaseModel):
#     departure_airport: Optional[str] = None
#     arrival_airport: Optional[str] = None
#     airport: Optional[str] = None
#     direction: Optional[FlightDirection] = None
#     origin_city: Optional[str] = None
#     destination_city: Optional[str] = None
#     date: Optional[str] = None
#     time_from: Optional[int] = None
#     time_to: Optional[int] = None
#     max_results: Optional[int] = None
#
#     @field_validator("*", mode="before")
#     @classmethod
#     def normalize_fields(cls, v):
#         if v in ("", None):
#             return None
#         if isinstance(v, str):
#             v = v.strip()
#             return v if v else None
#         return v
#
#     @field_validator("time_from", "time_to", mode="before")
#     @classmethod
#     def normalize_timestamps(cls, v):
#         if v in ("", None):
#             return None
#         return int(v)
#
#     @field_validator("time_from")
#     @classmethod
#     def validate_time_from(cls, v):
#         if v is None:
#             return None
#         now_ts = int(datetime.now(timezone.utc).timestamp())
#         if v < now_ts:
#             raise ValueError("time_from must be greater than or equal to now")
#         return v
#
#     @model_validator(mode="after")
#     def validate_time_window(self):
#         if self.time_from is not None and self.time_to is not None:
#             max_end = self.time_from + 12 * 60 * 60
#             if self.time_to > max_end:
#                 raise ValueError("time_to must be within 12 hours of time_from")
#             if self.time_to < self.time_from:
#                 raise ValueError("time_to must be greater than or equal to time_from")
#         return self

class SearchFlightsArgs(BaseModel):
    airport: str
    time_from: int
    time_to: int

    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    direction: Optional[FlightDirection] = None
    origin_city: Optional[str] = None
    destination_city: Optional[str] = None
    date: Optional[str] = None
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

    @field_validator("time_from", "time_to", mode="before")
    @classmethod
    def normalize_timestamps(cls, v):
        return int(v)

    @field_validator("airport", mode="before")
    @classmethod
    def validate_airport(cls, v):
        if not v:
            raise ValueError("airport is required")
        return v.strip().upper()

    @model_validator(mode="after")
    def validate_time_window(self):
        now_ts = int(datetime.now(timezone.utc).timestamp())
        if self.time_from < now_ts:
            raise ValueError("time_from must be greater than or equal to now")
        if self.time_to < self.time_from:
            raise ValueError("time_to must be greater than or equal to time_from")
        if self.time_to > self.time_from + 12 * 60 * 60:
            raise ValueError("time_to must be within 12 hours of time_from")
        return self

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
    time_from: Optional[int] = None
    time_to: Optional[int] = None
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