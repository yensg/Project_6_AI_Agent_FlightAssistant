# from typing import Optional
# from pydantic import BaseModel, Field
#
#
# class ExtractedEntities(BaseModel):
#     location: Optional[str] = None
#     activity_type: Optional[str] = None
#     date: Optional[str] = None
#     participants: Optional[int] = None
#     departure_airport: Optional[str] = None
#     arrival_airport: Optional[str] = None
#
#
# class ExtractedPreferences(BaseModel):
#     budget: Optional[str] = None
#     family_friendly: Optional[bool] = None
#
#
# class ExtractedMemory(BaseModel):
#     traveling_with_children: Optional[bool] = None
#
#
# class ExtractedMessageData(BaseModel):
#     intent: Optional[str] = None
#     entities: ExtractedEntities = Field(default_factory=ExtractedEntities)
#     preferences: ExtractedPreferences = Field(default_factory=ExtractedPreferences)
#     memory: ExtractedMemory = Field(default_factory=ExtractedMemory)

# src/schemas/context/typed_schema.py

from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


FlightIntent = Literal[
    "get_flight_details",
    "search_flights",
    "count_flights",
    "list_flights",
    "clarify"
]

FlightDirection = Literal["arrival", "departure"]
FlightDay = Literal["today", "tomorrow", "yesterday"]
AggregationType = Literal[
    "count",
    "group_by_airline",
    "group_by_origin",
    "group_by_destination",
    "none"
]
ResponseMode = Literal["summary", "detailed"]


class ExtractedEntities(BaseModel):
    flight_number: Optional[str] = None
    callsign: Optional[str] = None
    icao24: Optional[str] = None
    airline: Optional[str] = None

    airport: Optional[str] = None
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    direction: Optional[FlightDirection] = None

    origin_city: Optional[str] = None
    destination_city: Optional[str] = None

    date: Optional[str] = None
    local_day: Optional[FlightDay] = None
    time_from: Optional[str] = None
    time_to: Optional[str] = None

    @field_validator(
        "flight_number",
        "callsign",
        "icao24",
        "airline",
        "airport",
        "departure_airport",
        "arrival_airport",
        "origin_city",
        "destination_city",
        "date",
        "time_from",
        "time_to",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, value: Optional[Any]) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned if cleaned else None
        return str(value).strip() or None


class ExtractedPreferences(BaseModel):
    timezone: Optional[str] = None
    response_mode: Optional[ResponseMode] = None
    max_results: Optional[int] = None

    @field_validator("timezone", mode="before")
    @classmethod
    def normalize_timezone(cls, value: Optional[Any]) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned if cleaned else None
        return str(value).strip() or None

    @field_validator("max_results", mode="before")
    @classmethod
    def validate_max_results(cls, value: Optional[Any]) -> Optional[int]:
        if value in (None, ""):
            return None
        int_value = int(value)
        if int_value < 1:
            raise ValueError("max_results must be >= 1")
        return int_value


class InferredDefaults(BaseModel):
    airport: Optional[str] = None
    direction: Optional[FlightDirection] = None

    @field_validator("airport", mode="before")
    @classmethod
    def normalize_airport(cls, value: Optional[Any]) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned if cleaned else None
        return str(value).strip() or None


class ContextUpdate(BaseModel):
    domain: Optional[str] = "flight"
    intent: Optional[FlightIntent] = None
    entities: ExtractedEntities = Field(default_factory=ExtractedEntities)
    aggregation: AggregationType = "none"
    preferences: ExtractedPreferences = Field(default_factory=ExtractedPreferences)
    inferred_defaults: InferredDefaults = Field(default_factory=InferredDefaults)
    missing_slots: List[str] = Field(default_factory=list)
    requires_tool: Optional[bool] = None
    confidence: Optional[float] = None

    @field_validator("domain", mode="before")
    @classmethod
    def normalize_domain(cls, value: Optional[Any]) -> Optional[str]:
        if value is None:
            return "flight"
        if isinstance(value, str):
            cleaned = value.strip().lower()
            return cleaned if cleaned else "flight"
        return "flight"

    @field_validator("missing_slots", mode="before")
    @classmethod
    def normalize_missing_slots(cls, value: Optional[Any]) -> List[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]
        return [str(value).strip()] if str(value).strip() else []

    @field_validator("confidence", mode="before")
    @classmethod
    def validate_confidence(cls, value: Optional[Any]) -> Optional[float]:
        if value in (None, ""):
            return None
        float_value = float(value)
        if not 0.0 <= float_value <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        return float_value


class ConversationContext(BaseModel):
    active_domain: str = "flight"
    last_intent: Optional[FlightIntent] = None
    last_entities: Dict[str, Any] = Field(default_factory=dict)
    preferences: Dict[str, Any] = Field(default_factory=lambda: {
        "timezone": "Asia/Singapore",
        "response_mode": "summary",
        "max_results": 10
    })
    memory: Dict[str, Any] = Field(default_factory=lambda: {
        "airport": "WSSS"
    })
    unresolved_slots: List[str] = Field(default_factory=list)