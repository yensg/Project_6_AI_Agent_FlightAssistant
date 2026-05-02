from semantic_kernel.functions import kernel_function
from typing import Dict, Any
import httpx
import logging

from ..core.config import get_settings
from ..utils.logger import setup_logger

# API_FLIGHT_URL = "https://opensky-network.org/api/flights/all"
# HEADERS = {
#     "Accept": "application/json"
# }

logger = setup_logger(__name__)

class FlightSkill:
    # def __init__(self, kernel):
    #     self.kernel = kernel
    #
    #     # Register functions into kernel
    #     self.kernel.add_function(self.get_flight_details)
    #     self.kernel.add_function(self.search_flights)
    #     self.kernel.add_function(self.count_flights)
    #     self.kernel.add_function(self.list_flights)

    # API_FLIGHT_URL = "https://opensky-network.org/api/flights/all"
    API_FLIGHT_URL = "http://api.aviationstack.com/v1/flights"
    HEADERS = {
        "Accept": "application/json"
    }

    # @kernel_function(name="search_flights", description="Search flights for a required airport and time window")
    # async def search_flights(
    #     self,
    #     departure_airport: str | None = None,
    #     arrival_airport: str | None = None,
    #     airport: str | None = None,
    #     direction: str | None = None,
    #     origin_city: str | None = None,
    #     destination_city: str | None = None,
    #     date: str | None = None,
    #     time_from: str | None = None,
    #     time_to: str | None = None,
    #     max_results: int | None = 10,
    # ) -> Dict[str, Any]:
    #     return {
    #         "matches": [],
    #         "filters": {
    #             "departure_airport": departure_airport,
    #             "arrival_airport": arrival_airport,
    #             "airport": airport,
    #             "direction": direction,
    #             "origin_city": origin_city,
    #             "destination_city": destination_city,
    #             "date": date,
    #             "time_from": time_from,
    #             "time_to": time_to,
    #             "max_results": max_results,
    #         }
    #     }

    @kernel_function(
        name="search_flights",
        description="Search flights arriving at or departing from an airport using IATA airport code"
    )
    # @kernel_function(name="search_flights", description="Search recent/current flights arriving at an airport using IATA airport code")
    async def search_flights(
        self,
        # airport: str,
        # time_from: int,
        # time_to: int,
        # departure_airport: str | None = None,
        # arrival_airport: str | None = None,
        # direction: str | None = None,
        # origin_city: str | None = None,
        # destination_city: str | None = None,
        # date: str | None = None,
        airport: str = "SIN",
        direction: str = "arrival",
        max_results: int | None = 5,

    ) -> Dict[str, Any]:
        # params = {
        #     "airport": "WSSS",
        #     "begin": time_from,
        #     "end": time_to,
        # }
        settings = get_settings()

        params = {
            "access_key": settings.aviationstack_access_key,
            # "arr_iata": airport,
            "limit": max_results or 5,
        }

        if direction == "departure":
            params["dep_iata"] = airport
        else:
            params["arr_iata"] = airport


        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    self.API_FLIGHT_URL,
                    params=params,
                    headers=self.HEADERS
                )
                response.raise_for_status()
                data = response.json()

                flights = data.get("data", [])

                logger.info(f"API success, received {len(flights) if isinstance(flights, list) else 'unknown'} records")

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
                return {
                    "airport": airport,
                    "direction": direction,
                    "count": 0,
                    "flights": [],
                    "error": f"API error {e.response.status_code}"
                }

            except httpx.RequestError as e:
                logger.error(f"Network error: {str(e)}")
                return {
                    "airport": airport,
                    "direction": direction,
                    "count": 0,
                    "flights": [],
                    "error": "Network error"
                }

            except ValueError as e:
                logger.error(f"JSON parse error: {str(e)}")
                return {
                    "airport": airport,
                    "direction": direction,
                    "count": 0,
                    "flights": [],
                    "error": "Invalid JSON response"
                }

            # this is bad
            # except Exception as e:
            #     logger.error(f"Unexpected error: {str(e)}")
            #     return {
            #         "airport": airport,
            #         "count": 0,
            #         "flights": [],
            #         "error": str(e),
            #     }

        if not isinstance(flights, list):
            logger.warning("Unexpected API response format")
            return {
                "airport": airport,
                "direction": direction,
                "count": 0,
                "flights": [],
                "message": "Unexpected API response format"
            }

        return {
            "airport": airport,
            "direction": direction,
            "count": len(flights),
            # "flights": data[:max_results] if max_results else data
            "flights": flights
        }

    # @kernel_function(name="get_flight_details", description="Get details of a flight")
    # async def get_flight_details(
    #     self,
    #     flight_number: str | None = None,
    #     callsign: str | None = None,
    #     icao24: str | None = None,
    #     date: str | None = None,
    #     airport: str | None = None,
    # ) -> Dict[str, Any]:
    #     return {
    #         "flight_number": flight_number,
    #         "callsign": callsign,
    #         "icao24": icao24,
    #         "date": date,
    #         "airport": airport,
    #         "status": "scheduled"
    #     }
    #
    # @kernel_function(name="count_flights", description="Count flights")
    # async def count_flights(
    #     self,
    #     airport: str | None = None,
    #     direction: str | None = None,
    #     departure_airport: str | None = None,
    #     arrival_airport: str | None = None,
    #     date: str | None = None,
    # ) -> Dict[str, Any]:
    #     return {
    #         "count": 0,
    #         "filters": {
    #             "airport": airport,
    #             "direction": direction,
    #             "departure_airport": departure_airport,
    #             "arrival_airport": arrival_airport,
    #             "date": date,
    #         }
    #     }
    #
    # @kernel_function(name="list_flights", description="List flights")
    # async def list_flights(
    #     self,
    #     airport: str | None = None,
    #     direction: str | None = None,
    #     departure_airport: str | None = None,
    #     arrival_airport: str | None = None,
    #     date: str | None = None,
    #     time_from: str | None = None,
    #     time_to: str | None = None,
    #     max_results: int | None = 10,
    # ) -> Dict[str, Any]:
    #     return {
    #         "flights": [],
    #         "filters": {
    #             "airport": airport,
    #             "direction": direction,
    #             "departure_airport": departure_airport,
    #             "arrival_airport": arrival_airport,
    #             "date": date,
    #             "time_from": time_from,
    #             "time_to": time_to,
    #             "max_results": max_results,
    #         }
    #     }